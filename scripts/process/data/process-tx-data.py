import gzip
import json
import pandas as pd
import os
from os import path
from multiprocessing import Pool, cpu_count
from transactions.constants import DATA_PATH, RESULTS_PATH

import zlib

def process_file_to_df(filename):
    transactions = []
    try:
        with gzip.open(os.path.join(DATA_PATH, filename), "rt") as file:
            print(file)
            for line in file:
                try:
                    record = json.loads(line)
                    transactions.append(record)
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error in file {filename}: {e}")
    except zlib.error as e:
        print(f"Zlib Error in file {filename}: {e}")
        return None  
    except Exception as e:  # This is to catch any other unexpected errors
        print(f"Unexpected error in file {filename}: {e}")
        return None  

    return pd.DataFrame(transactions)



if __name__ == '__main__':

    num_cores = cpu_count() - 1

    file_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".jsonl.gz")]
    print(file_list)

    with Pool(num_cores) as pool:
        df_list = list(pool.map(process_file_to_df, file_list))
    
    print('concat')
    df = pd.concat(df_list, ignore_index=True)
   
    df.to_csv(os.path.join(DATA_PATH, "transactions-data-test.csv"), index=False)
   