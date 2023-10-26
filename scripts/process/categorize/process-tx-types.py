import gzip
import json
import pandas as pd
import os
from multiprocessing import Pool, cpu_count
from transactions.constants import DATA_PATH, RESULTS_PATH

def identify_transaction_types(df):
    transaction_counts = df['name'].value_counts()
    transaction_percentages = (transaction_counts / len(df)) * 100

    transactions_types_df = pd.DataFrame({
        'Transaction type': transaction_counts.index,
        'Count': transaction_counts.values,
        'Percentage': transaction_percentages
    })

    return transactions_types_df

# Load the CSV file into a DataFrame
file_path = os.path.join(DATA_PATH, 'transactions-data.csv')

df = pd.read_csv(file_path)

transactions_types_df = identify_transaction_types(df)

transactions_types_df.to_csv(os.path.join(RESULTS_PATH, "transaction_types.csv"), index=False)
