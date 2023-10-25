import pandas as pd
import os
import base64
from transactions.constants import DATA_PATH

# Function to decode base64
def decode_base64(base64_message):
    base64_bytes = base64_message.encode('utf-8')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf-8')

# Load the CSV file into a DataFrame
df = pd.read_csv(os.path.join(DATA_PATH, "transactions-data.csv"))

# Check each row in the 'memo_base64' column
for index, row in df.iterrows():
    # Check if 'memo_base64' is not NaN and not empty
    if pd.notna(row['memo_base64']) and row['memo_base64'].strip():
        # Decode base64 to string
        try:
            decoded_memo = decode_base64(row['memo_base64'])
            print(f"Row {index}: {decoded_memo}")
        except Exception as e:
            print(f"Could not decode base64 at row {index} due to: {str(e)}")
    else:
        print("Nothing found!")
