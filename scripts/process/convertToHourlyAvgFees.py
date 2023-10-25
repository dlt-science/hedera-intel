import pandas as pd
import os
from datetime import datetime
from os import path
from transactions.constants import DATA_PATH, RESULTS_PATH

# Load the CSV file
file_path = os.path.join(DATA_PATH, "timeseries_data_2020.csv")
df = pd.read_csv(file_path)

df['fee'] = pd.to_numeric(df['fee'], errors='coerce')

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'])

df['hour'] = df['time'].dt.strftime('%Y-%m-%d %H:00:00')

# Calculate average fees per hour for all types
hourly_avg_fees_all = df.groupby('hour')['fee'].mean().reset_index()

# Convert fees from tinybars to hbars
hourly_avg_fees_all['fee'] = hourly_avg_fees_all['fee'] / 100_000_000

# Rename the column
hourly_avg_fees_all = hourly_avg_fees_all.rename(columns={
    'hour': 'time'
})

print(hourly_avg_fees_all)

output_file_path_all = os.path.join(RESULTS_PATH, 'hourly_average_fees.csv')
hourly_avg_fees_all.to_csv(output_file_path_all, index=False)
