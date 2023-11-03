import pandas as pd
import ast
from collections import Counter
from transactions.constants import DATA_PATH, RESULTS_PATH
import os
import numpy as np
from multiprocessing import Pool, cpu_count

def count_transactions_chunk(chunk):
    def count_transactions(row):
        transfers_str = row['transfers']
        name = row['name']
        transfers = ast.literal_eval(transfers_str)
        counts = Counter()
        
        for transfer in transfers:
            if transfer['amount'] < 0:  # Counting senders
                account = transfer['account']
                counts[account] = counts.get(account, 0) + 1
                
        return pd.Series([counts, name], index=['Counts', 'Transaction Type'])

    return chunk.apply(count_transactions, axis=1)

if __name__ == '__main__':
    print("Reading CSV")
    df = pd.read_csv(os.path.join(DATA_PATH, 'transactions-data.csv'))
    chunks = np.array_split(df, cpu_count())

    print("Counting")
    with Pool(cpu_count()) as pool:
        results = pool.map(count_transactions_chunk, chunks)

    result = pd.concat(results)

    data = []
    for index, row in result.iterrows():
        for account, count in row['Counts'].items():
            data.append({
                "Address": account, 
                "Transaction Counts": count, 
                "Transaction Type": row['Transaction Type']
            })

    topAccounts_df = pd.DataFrame(data)

    print("Sorting")
    topAccounts_df = topAccounts_df.sort_values(by='Transaction Counts', ascending=False)

    print("Saving CSV")
    topAccounts_df.to_csv(os.path.join(RESULTS_PATH, 'top-accounts.csv'), index=False)
