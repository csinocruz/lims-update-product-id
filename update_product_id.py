import argparse
import pandas as pd
from s4.clarity import LIMS

BATCH_SIZE = 96

def parse_args() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_uri', '-r', metavar='STR', required=True, type=str,
                        help='The root API URI of form `https://test.lims.sdlb.helix.com/api/v2`')
    parser.add_argument('--username', '-u', metavar='STR', required=True, type=str)
    parser.add_argument('--password', '-p', metavar='STR', required=True, type=str)
    parser.add_argument('--file_name', '-f', metavar='STR', required=True, type=str)
    parser.add_argument('--product_id', '-pi', metavar='STR', required=True, type=str)
    args = parser.parse_args()

    return args

def main():

    #get command-line args
    args = parse_args()
    
    lims = LIMS(args.root_uri, args.username, args.password)
    
    for batch in pd.read_csv(args.file_name, header=None, chunksize=BATCH_SIZE):
        sample_list = []
        #makes list out of sample name column
        sample_list = list(batch[0])
        
        #by default prefetch=True and loads full content for each element returned by query
        samples = lims.samples.query(name=sample_list)
        
        #update ProductID udf with new ID
        for sample in samples:
            sample['ProductID'] = args.product_id
        
        #persists the samples back to Clarity
        lims.samples.batch_update(samples)
        print("Updating ProductID to: {0} for {1} samples".format(args.product_id, len(samples)))
        
        #TO-DO handle ClarityExceptions raised by batch_update

if __name__ == '__main__':
    main()

#00463219613571
#00882780410972
#01612129629392
#02911509513759