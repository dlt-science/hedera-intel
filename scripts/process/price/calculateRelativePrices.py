import pandas as pd
import os
from transactions.constants import DATA_PATH, RESULTS_PATH

cmc_df = pd.read_csv(os.path.join(RESULTS_PATH, "prices", "CMC_Crypto_Index.csv"))
hbar_df = pd.read_csv(os.path.join(RESULTS_PATH, "prices", "hbar_price_2023.csv"))

merged_df = pd.merge(cmc_df, hbar_df, on="time", suffixes=('_cmc', '_hbar'))

# Calculate the HBAR/ETH ratio
merged_df['HBAR/CMC'] = merged_df['price_hbar'] / merged_df['price_cmc']

output_df = merged_df[['time', 'HBAR/CMC']]

output_path  = os.path.join(RESULTS_PATH, "prices", "HBARvsCMC_price_2023.csv")

# Save the result to a new CSV file
output_df.to_csv(output_path, index=False)
