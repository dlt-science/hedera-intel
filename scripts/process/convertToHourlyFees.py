import pandas as pd
import os
from datetime import datetime
from os import path
from transactions.constants import DATA_PATH, RESULTS_PATH

# Load the CSV file
file_path = os.path.join(DATA_PATH, "timeseries_data.csv")
df = pd.read_csv(file_path)

df['fee'] = pd.to_numeric(df['fee'], errors='coerce')

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'])

df['hour'] = df['time'].dt.strftime('%Y-%m-%d %H:00:00')

hourly_avg_fees = df.groupby(['hour', 'type'])['fee'].mean().unstack(fill_value=0).reset_index()

# Rename the column
hourly_avg_fees = hourly_avg_fees.rename(columns={
    'hour': 'time'
})

print(hourly_avg_fees)

output_file_path = os.path.join(RESULTS_PATH, 'hourly_average_fees.csv')
hourly_avg_fees.to_csv(output_file_path, index=False)
