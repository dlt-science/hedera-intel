import pandas as pd
import ast
import os
from transactions.constants import DATA_PATH, RESULTS_PATH


df = pd.read_csv(os.path.join(DATA_PATH, "data_ct_1y", "data_ct_1y.csv"))


consensus_timestamps = []
charged_tx_fees = []
transaction_ids = []
from_accounts = []
to_accounts = []
amounts = []
trx_to_inspect = []

def process_row(row):
    try:
        
        time = int(str(row['consensus_timestamp']).split('.')[0])

        # Convert to a datetime
        timestamp = pd.to_datetime(time, unit='s')

        # Decode and evaluate the "transfers" column to get it as a list
        transfers = ast.literal_eval(row['transfers'])

        # If transfers is empty, return None
        if not transfers:
            return None

        # Extract unique sender accounts 
        sender_accounts = [transfer['account'] for transfer in transfers if transfer['amount'] < 0]

        # Check if there are more than two different accounts with negative amounts
        if len(set(sender_accounts)) >= 2:
            return {'transaction_id': row['transaction_id'], 'type': 'inspect'}
        else:
            from_account = sender_accounts[0]
            results = [{'time': timestamp, 'fee': row['charged_tx_fee'], 'transaction_id': row['transaction_id'],
                        'from': from_account, 'to': transfer['account'], 'amount': transfer['amount']} 
                       for transfer in transfers if transfer['amount'] > 0]
            return results
    except ValueError:
        print(f"Problematic row: {row}")
        return None

results = df.apply(process_row, axis=1)
trx_to_inspect = [x['transaction_id'] for x in results if isinstance(x, dict) and x['type'] == 'inspect']
processed_data = [item for sublist in results.dropna() if isinstance(sublist, list) for item in sublist]

# Save the complex transactions for further inspection
pd.DataFrame({'transaction_id': trx_to_inspect}).to_csv(os.path.join(RESULTS_PATH, "graphs", "trx_to_inspect1y.csv"), index=False)

# Save the processed data
result_df = pd.DataFrame(processed_data)
result_df = result_df.sort_values(by="time")
result_df.to_csv(os.path.join(RESULTS_PATH, "graphs", "transactions-data_ct_1y.csv"), index=False)
