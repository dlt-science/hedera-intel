import pandas as pd
import os
from os import path
from datetime import datetime
from transactions.constants import DATA_PATH, RESULTS_PATH

# Load the CSV file
df = pd.read_csv(os.path.join(DATA_PATH, "timeseries_data.csv"))

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'])

df['hour'] = df['time'].dt.strftime('%Y-%m-%d %H:00:00')

hourly_data_counts = df.groupby(['hour', 'type']).size().unstack(fill_value=0)

hourly_data_counts.reset_index(inplace=True)

hourly_data_counts = hourly_data_counts.rename(columns={
    'hour': 'time'
})

print(hourly_data_counts)

output_file_path = os.path.join(RESULTS_PATH, 'hourly_data_counts.csv')
hourly_data_counts.to_csv(output_file_path, index=False)
