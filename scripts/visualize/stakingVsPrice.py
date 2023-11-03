import pandas as pd
import altair as alt
import os
from transactions.constants import DATA_PATH, RESULTS_PATH, FIGURES_PATH

prices_path = os.path.join(RESULTS_PATH, "prices", "HBARvsETH_price_2023.csv")
stakes_path = os.path.join(RESULTS_PATH, "nodes", "nodes_historical_stakes.csv")

df_prices = pd.read_csv(prices_path)
df_stakes = pd.read_csv(stakes_path)

# Convert the "time" columns to a common datetime format
df_prices["time"] = pd.to_datetime(df_prices["time"])
df_stakes["time"] = pd.to_datetime(df_stakes["time"])

# Merge the two DataFrames on the standardized "time" column
df = pd.merge(df_prices, df_stakes, on="time")

# Base chart
base = alt.Chart(df).encode(
    x=alt.X("time:T", title="Time")
).properties(
    width=600
)

# Define buffer for y-axis range
price_buffer = (df["price"].max() - df["price"].min()) * 0.1
stake_buffer = (df["stake_amount"].max() - df["stake_amount"].min()) * 0.1

# Line for HBAR/ETH Price
price_line = base.mark_line().encode(
    y=alt.Y("price:Q", title="HBAR/ETH Price", scale=alt.Scale(domain=[df["price"].min() - price_buffer, df["price"].max() + price_buffer])),
    color=alt.value("blue"),
    tooltip="price:Q"
)

# Line for HBAR Total Staked on a separate Y axis
stake_line = base.mark_line().encode(
    y=alt.Y("stake_amount:Q", axis=alt.Axis(title="HBAR Total Staked"), scale=alt.Scale(domain=[df["stake_amount"].min() - stake_buffer, df["stake_amount"].max() + stake_buffer])),
    color=alt.value("green"),
    tooltip="stake_amount:Q"
)

# Save the chart
chart.save('stakingVsPriceRelative.html')



