import argparse
import os
import pandas as pd
from s4.clarity import LIMS
from s4.clarity import exception
import sys
from requests.exceptions import ConnectionError

BATCH_SIZE = 96

def parse_args() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_uri', required=True, type=str,
                        help='The root API URI of form `https://test.lims.sdlb.helix.com/api/v2`')
    parser.add_argument('--username', '-u', required=True, type=str,
                        help='Clarity LIMS Username - requires API permissions')
    parser.add_argument('--password', '-p', required=True, type=str, 
                        help='Clarity LIMS Password')
    parser.add_argument('--file_name', '-f', required=True, type=str)
    parser.add_argument('--product_id', required=True, type=str)
    args = parser.parse_args()

    return args

def print_samples(sl):
    for i, sample in enumerate(sl):
        print("{0}: {1}".format(i+1, sample))

def main():

    #get command-line args
    args = parse_args()
    
    #check file exists
    if not os.path.isfile(args.file_name):
        print("{0} cannot be found.".format(args.file_name))
        sys.exit(1)

    #keep list of samples 
    samples_not_updated = []

    #reads samples into batches of 96
    for batch in pd.read_csv(args.file_name, header=None, chunksize=BATCH_SIZE):
        sample_batch = []
        #makes list out of sample name column
        sample_batch = list(batch[0])
        
        #keep list of samples as they are updated
        updated_samples = []
        
        lims = LIMS(args.root_uri, args.username, args.password)

        try:
            #fetch samples from LIMS
            #by default prefetch=True, so query() loads full content for each sample returned
            samples = lims.samples.query(name=sample_batch) 
        
        except exception.ClarityAuthenticationException as e:
            print("Check username/password:", e)
            sys.exit(1)
        except exception.ClarityException as e:
            print("Unable to query LIMS: ", e)
            sys.exit(1)
        except ConnectionError as e:
            print("Connection Error: ", e.args[0].reason)
            sys.exit(1)

        #update ProductID udf with new ID
        for sample in samples:
            sample['ProductID'] = args.product_id
            updated_samples.append(sample.name)
            
        try:
            #persists the samples back to Clarity
            lims.samples.batch_update(samples)
            print("Updating ProductID to: {0} for {1} samples".format(args.product_id, len(samples)))
        except exception.ClarityException as e:
            print(e)
            sys.exit(1)

        #identify samples not updated
        samples_not_found = set(sample_batch).difference(updated_samples)
        samples_not_updated.extend(list(samples_not_found))
    
    print("The following {} sample(s) were not updated:".format(len(samples_not_updated)))
    print_samples(samples_not_updated)

if __name__ == '__main__':
    main()
