import dask.dataframe as dd
import pandas as pd
import ast
from collections import Counter
from transactions.constants import DATA_PATH, RESULTS_PATH

print("Reading CSV")
# Use Dask to read the CSV
ddf = dd.read_csv(os.path.join(DATA_PATH, 'transactions-data.csv'))

def count_transactions(transfers_str, name):
    transfers = ast.literal_eval(transfers_str)
    counts = Counter()
    
    for transfer in transfers:
        if transfer['amount'] < 0:  # Counting senders
            account = transfer['account']
            counts[account] = counts.get(account, 0) + 1
            
    return pd.Series([counts, name], index=['Counts', 'Transaction Type'])

print("Counting")
# Compute results using Dask and then convert to Pandas DataFrame
result = ddf.map_partitions(lambda df: df.apply(
    lambda row: count_transactions(row['transfers'], row['name']), axis=1)).compute()

# Flattening the data
data = []
for index, row in result.iterrows():
    for account, count in row['Counts'].items():
        data.append({
            "Address": account, 
            "Transaction Counts": count, 
            "Transaction Type": row['Transaction Type']
        })

topWallets_df = pd.DataFrame(data)

print("Sorting")
topWallets_df = topWallets_df.sort_values(by='Transaction Counts', ascending=False)

print("Saving CSV")
topWallets_df.to_csv(os.path.join(RESULTS_PATH, 'top-wallets.csv'), index=False)
