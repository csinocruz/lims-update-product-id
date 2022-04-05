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
    print("Verifying ProductID's updated successfully...")
    #get command-line args
    args = parse_args()
    #print("-u {0} -p {1} -r {2} -f {3}".format(args.username, args.password, args.root_uri, args.file_name))
    lims = LIMS(args.root_uri, args.username, args.password)
    
    failed_samples = []

    for batch in pd.read_csv(args.file_name, header=None, chunksize=BATCH_SIZE):
        sample_list = []
        sample_list = list(batch[0])
        
        #by default prefetch=True and loads full content for each element returned by query
        samples = lims.samples.query(name=sample_list)
        
        for sample in samples:
            if sample['ProductID'] != args.product_id:
                failed_samples.append(sample)
    
    if len(failed_samples) == 0:
        print("Product ID update was successful.")
    else:
        print("{0} samples have the incorrect productID:".format(len(failed_samples)))
        for sample in failed_samples:
            print("  {0}".format(sample.name))
        
if __name__ == '__main__':
    main()