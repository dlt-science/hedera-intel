import pandas as pd
import ast
import datetime
import os
from collections import defaultdict
from transactions.constants import DATA_PATH, RESULTS_PATH

df = pd.read_csv(os.path.join(DATA_PATH, "transactions-data-ct.csv"))

# List to store the transactions needed to inspect manually
trx_to_inspect = []

# Lists to store the processed data
consensus_timestamps = []
charged_tx_fees = []
transaction_ids = []
from_accounts = []
to_accounts = []
amounts = []

for _, row in df.iterrows():
    try:
        # Extract the whole part of the consensus_timestamp (before the dot)
        whole_part = int(str(row['consensus_timestamp']).split('.')[0])
        
        # Convert the whole part to a datetime
        timestamp = datetime.datetime.fromtimestamp(whole_part).strftime('%Y-%m-%d %H:%M:%S')
        
        # Decode and evaluate the "transfers" column to get it as a list
        transfers = ast.literal_eval(row['transfers'])

        # If transfers is empty, skip the row
        if not transfers:
            continue

        # Extract unique accounts with negative amounts
        negative_accounts = [transfer['account'] for transfer in transfers if transfer['amount'] < 0]

        # Check if there are more than two different accounts with negative amounts
        account_counts = defaultdict(int)
        for account in negative_accounts:
            account_counts[account] += 1

        if len(account_counts) > 2:
            trx_to_inspect.append(row['transaction_id'])
        else:
            from_account = next(iter(account_counts.keys()))
            for transfer in transfers:
                if transfer['amount'] > 0:
                    consensus_timestamps.append(timestamp)
                    charged_tx_fees.append(row['charged_tx_fee'])
                    transaction_ids.append(row['transaction_id'])
                    from_accounts.append(from_account)
                    to_accounts.append(transfer['account'])
                    amounts.append(transfer['amount'])
    except ValueError:
        # Print the problematic row if there's an error in conversion
        print(f"Problematic row: {row}")
        continue

# Save the weird transactions
pd.DataFrame({'transaction_id': trx_to_inspect}).to_csv(os.path.join(RESULTS_PATH, "graphs", "trx_to_inspect.csv"), index=False)

# Save the processed data
result_df = pd.DataFrame({
    'consensus_timestamp': consensus_timestamps,
    'charged_tx_fee': charged_tx_fees,
    'transaction_id': transaction_ids,
    'from': from_accounts,
    'to': to_accounts,
    'amount': amounts
})

result_df = result_df.sort_values(by="consensus_timestamp")

result_df.to_csv(os.path.join(RESULTS_PATH, "graphs", "ct_data.csv"), index=False)
