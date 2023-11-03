import pandas as pd
import os
import base64
from transactions.constants import DATA_PATH, RESULTS_PATH

# Function to decode base64
def decode_base64(base64_message):
    base64_bytes = base64_message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')


# Load the CSV file into a DataFrame
df = pd.read_csv(os.path.join(DATA_PATH, "data_ct_1y", "data_ct_1y.csv"))

all_memos = []
suspicious_memos = []
unique_accounts = set()

# Keywords to look for
keywords = ['airdrop', 'claim', 'distribution']

# Check each row in the 'memo_base64' column
for index, row in df.iterrows():
    if pd.notna(row['memo_base64']) and row['memo_base64'].strip():
        try:
            decoded_memo = decode_base64(row['memo_base64'])
            all_memos.append(decoded_memo)

            if any(keyword in decoded_memo for keyword in keywords):
                suspicious_memos.append({
                    'memo': decoded_memo,
                    'consensus_timestamp': row['consensus_timestamp'],
                    'transaction_id': row['transaction_id']
                })

                transfers = eval(row['transfers'])
                for transfer in transfers:
                    if transfer['amount'] < 0:
                        unique_accounts.add(transfer['account'])

        except Exception as e:
            print(f"Could not decode base64 at row {index} due to: {str(e)}")

print(f"Number of unique sender accounts in suspicious transactions: {len(unique_accounts)}")

# Save all memos to AllMemo.csv
pd.DataFrame(all_memos, columns=['memo']).to_csv(os.path.join(RESULTS_PATH, "memos", 'AllMemo.csv'), index=False)
print(f"Count of memos in AllMemo.csv: {len(all_memos)}")

# Save suspicious memos to SuspiciousMemo.csv
pd.DataFrame(suspicious_memos).to_csv(os.path.join(RESULTS_PATH, "memos",  'SuspiciousMemo.csv'), index=False)
print(f"Count of memos in SuspiciousMemo.csv: {len(suspicious_memos)}")

# Save unique accounts in suspicious transactions to a CSV file
pd.DataFrame(list(unique_accounts), columns=['account']).to_csv(os.path.join(RESULTS_PATH, "memos", "ScammerAccounts.csv"), index=False)
