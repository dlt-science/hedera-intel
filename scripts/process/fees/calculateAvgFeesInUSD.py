import pandas as pd
import os
from transactions.constants import DATA_PATH, RESULTS_PATH

# Paths to the CSV files
prices_path = os.path.join(RESULTS_PATH, "hbar_price.csv")
fees_path = os.path.join(RESULTS_PATH, "hourly_average_fees.csv")

# Load the CSV files into pandas DataFrames
df_prices = pd.read_csv(prices_path)
df_fees = pd.read_csv(fees_path)

# Convert the "time" columns to a common datetime format
df_prices["time"] = pd.to_datetime(df_prices["time"]).dt.strftime('%Y-%m-%d %H:%M:%S')
df_fees["time"] = pd.to_datetime(df_fees["time"]).dt.strftime('%Y-%m-%d %H:%M:%S')

# Merge the two DataFrames on the standardized "time" column
merged_df = pd.merge(df_prices, df_fees, on="time")

# Multiply the "price" and "fee" columns to get the fee in USD
merged_df["fee_USD"] = merged_df["price"].astype(float) * merged_df["fee"].astype(float)

# Create a new DataFrame with only "time" and "fee_USD" columns
result_df = merged_df[["time", "fee_USD"]]

# Save the resulting DataFrame to a new CSV file
result_df.to_csv(os.path.join(RESULTS_PATH, "hourly_average_fees_USD.csv"), index=False)
