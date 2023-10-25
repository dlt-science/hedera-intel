import json
import pandas as pd
import os
from transactions.constants import DATA_PATH, RESULTS_PATH

file_path = os.path.join(DATA_PATH, "hbar_price.json")

# Load the JSON file
with open(file_path, "r") as file:
    data = json.load(file)

# Extract relevant data
prices = [{"time": entry["time"], "price": entry["principal_market_price_usd"]} for entry in data["data"]]

# Convert to DataFrame
df = pd.DataFrame(prices)

# Save to CSV
output_file = os.path.join(RESULTS_PATH, 'hbar_price.csv')
df.to_csv(output_file, index=False)
