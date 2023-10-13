import gzip
import json
import pandas as pd
import os
from multiprocessing import Pool, cpu_count
from transactions.constants import DATA_PATH, RESULTS_PATH

def process_file_to_df(filename):
    transactions = []
    with gzip.open(os.path.join(DATA_PATH, filename), "rt") as file:
        for line in file:
            try:
                record = json.loads(line)
                transactions.append(record)
            except json.JSONDecodeError as e:
                print(f"Error in file {filename}: {e}")

    return pd.DataFrame(transactions)

def identify_transaction_types(df):
    transaction_counts = df['name'].value_counts()
    transaction_percentages = (transaction_counts / len(df)) * 100

    transactions_types_df = pd.DataFrame({
        'Transaction type': transaction_counts.index,
        'Count': transaction_counts.values,
        'Percentage': transaction_percentages
    })

    return transactions_types_df

if __name__ == '__main__':

    num_cores = cpu_count()

    file_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".jsonl.gz")]

    with Pool(num_cores) as pool:
        df_list = list(pool.map(process_file_to_df, file_list))

    df = pd.concat(df_list, ignore_index=True)
   
    df.to_csv(os.path.join(DATA_PATH, "transactions-data.csv"), index=False)
   
    transactions_types_df = identify_transaction_types(df)

    transactions_types_df.to_csv(os.path.join(RESULTS_PATH, "transaction_types.csv"), index=False)
