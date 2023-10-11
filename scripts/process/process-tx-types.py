import gzip
import json
import pandas as pd
import os
from multiprocessing import Pool, cpu_count
from transactions.constants import DATA_PATH, RESULTS_PATH

# Function to process each file and return a DataFrame
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

if __name__ == '__main__':

    num_cores = cpu_count()

    file_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".jsonl.gz")]

    # Use multiprocessing 
    with Pool(num_cores) as pool:
        df_list = list(pool.map(process_file_to_df, file_list))

    df = pd.concat(df_list, ignore_index=True)

    transaction_counts = df['name'].value_counts()
    transaction_percentages = (transaction_counts / len(df)) * 100

    transactions_types_df = pd.DataFrame({
        'Transaction type': transaction_counts.index,
        'Count': transaction_counts.values,
        'Percentage': transaction_percentages
    })

    # Save to a CSV
    transactions_types_df.to_csv(os.path.join(RESULTS_PATH, "transaction_types.csv"), index=False)

