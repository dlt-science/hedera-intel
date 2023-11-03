import pandas as pd
import os
from transactions.constants import DATA_PATH, RESULTS_PATH

# Load the CSV files into DataFrames
eth_df = pd.read_csv(os.path.join(RESULTS_PATH, "prices", "eth_price_2023.csv"))
hbar_df = pd.read_csv(os.path.join(RESULTS_PATH, "prices", "hbar_price_2023.csv"))

# Merge the DataFrames on the "time" column
merged_df = pd.merge(eth_df, hbar_df, on="time", suffixes=('_eth', '_hbar'))

# Calculate the HBAR/ETH ratio
merged_df['HBAR/ETH'] = merged_df['price_hbar'] / merged_df['price_eth']

output_df = merged_df[['time', 'HBAR/ETH']]

output_path  = os.path.join(RESULTS_PATH, "prices", "HBARvsETH_price_2023.csv")

# Save the result to a new CSV file
output_df.to_csv(output_path, index=False)
