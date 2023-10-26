import requests
import csv
import os
from datetime import datetime, timedelta
from transactions.constants import RESULTS_PATH

# Node account_ID
nodeID = "0.0.09"

# Define the API URL
url = f"https://mainnet-public.mirrornode.hedera.com/api/v1/balances?account.id={nodeID}"

# Define the start and end timestamps for the historical data (daily data)
start_date = datetime(2023, 7, 1)
end_date = datetime(2023, 10, 26)

# Initialize a list to store the data
data_list = []

# Fetch data for each day in the specified date range
current_date = start_date
while current_date <= end_date:
    # Convert the date to a Unix timestamp
    timestamp = int(current_date.timestamp())

    # Make the API request
    response = requests.get(f"{url}&timestamp={timestamp}")

    if response.status_code == 200:
        data = response.json()
        balance = data["balances"][0]["balance"]
        data_list.append([current_date.strftime("%Y-%m-%d"), balance])
    else:
        print(f"Failed to fetch data for {current_date.strftime('%Y-%m-%d')}")

    # Move to the next day
    current_date = current_date + timedelta(days=1)

# Specify the folder and filename
csv_filename = os.path.join(RESULTS_PATH, "node_balances", f"historical_balance_{nodeID}.csv")

# Save the data to a CSV file
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)  # Create the folder if it doesn't exist
with open(csv_filename, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Date", "Balance"])
    csv_writer.writerows(data_list)

print(f"Data saved to {csv_filename}")
