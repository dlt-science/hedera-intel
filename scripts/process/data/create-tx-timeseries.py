import gzip
import json
import pandas as pd
import os
from os import path
from datetime import datetime, timezone
from multiprocessing import Pool, cpu_count
from transactions.constants import DATA_PATH, RESULTS_PATH

# Function to convert epoch to human-readable date
def convert_epoch_to_date(epoch):
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

# Load the CSV file into a DataFrame
file_path = os.path.join(DATA_PATH, 'transactions-data-test.csv')

df = pd.read_csv(file_path, low_memory=False, usecols=['consensus_timestamp', 'name', 'charged_tx_fee'])

# Convert consensus_timestamp to human-readable date
df['consensus_timestamp'] = df['consensus_timestamp'].apply(lambda x: convert_epoch_to_date(x)) 

df = df.sort_values(by='consensus_timestamp')

print(df.head())

time_series_df = df[['consensus_timestamp', 'name', 'charged_tx_fee']]

# Rename the columns
time_series_df = time_series_df.rename(columns={
    'consensus_timestamp': 'time',
    'name': 'type',
    'charged_tx_fee': 'fee'  
})

# Save to a new CSV file
time_series_df.to_csv(os.path.join(DATA_PATH, "timeseries_data__test.csv"), index=False)
