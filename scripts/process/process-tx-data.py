import gzip
import json
import pandas as pd
import os
from os import path
from multiprocessing import Pool, cpu_count
from transactions.constants import DATA_PATH, RESULTS_PATH


def process_file_to_df(filename):
    transactions = []
    with gzip.open(os.path.join(DATA_PATH, filename), "rt") as file:
        print(file)
        for line in file:
            try:
                record = json.loads(line)
                transactions.append(record)
            except json.JSONDecodeError as e:
                print(f"Error in file {filename}: {e}")

    return pd.DataFrame(transactions)


if __name__ == '__main__':

    num_cores = cpu_count()

    file_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".jsonl.gz")]
    print(file_list)

    with Pool(num_cores) as pool:
        df_list = list(pool.map(process_file_to_df, file_list))
    
    print('concat')
    df = pd.concat(df_list, ignore_index=True)
   
    df.to_csv(os.path.join(DATA_PATH, "transactions-data.csv"), index=False)
   