import pandas as pd
import altair as alt
import os
from scipy.stats import pearsonr
from transactions.constants import DATA_PATH, RESULTS_PATH, FIGURES_PATH

prices_path = os.path.join(RESULTS_PATH, "prices", "HBARvsCMC_price_2023.csv")
stakes_path = os.path.join(RESULTS_PATH, "nodes", "nodes_historical_stakes.csv")

df_prices = pd.read_csv(prices_path)
df_stakes = pd.read_csv(stakes_path)

df_prices["time"] = pd.to_datetime(df_prices["time"])
df_stakes["time"] = pd.to_datetime(df_stakes["time"])

# Merge the two DataFrames on the standardized "time" column
df = pd.merge(df_prices, df_stakes, on="time")

# Calculate Pearson correlation coefficient and p-value
pearson_corr, p_value = pearsonr(df['hbar/cmc'], df['staked_amount'])
print(f"Pearson correlation: {pearson_corr:.2f}")
print(f"P-value: {p_value:.4f}") 


base = alt.Chart(df).encode(
    x=alt.X("time:T", title="Time")
).properties(
    width=600
)

# Define buffer for y-axis range
price_buffer = (df["hbar/cmc"].max() - df["hbar/cmc"].min()) * 0.1
stake_buffer = (df["staked_amount"].max() - df["staked_amount"].min()) * 0.1

# Line for HBAR/CMC Price
price_line = base.mark_line().encode(
    y=alt.Y("hbar/cmc:Q", title="HBAR/CMC Crypto Price", scale=alt.Scale(domain=[df["hbar/cmc"].min() - price_buffer, df["hbar/cmc"].max() + price_buffer])),
    color=alt.value("blue")
).properties(
    title="HBAR/CMC Crypto Price and Total Staked"
)

# Line for HBAR Total Staked on a separate Y axis
stake_line = base.mark_line().encode(
    y=alt.Y("staked_amount:Q", title="HBAR Total Staked", scale=alt.Scale(domain=[df["staked_amount"].min() - stake_buffer, df["staked_amount"].max() + stake_buffer])),
    color=alt.value("green")
)

# Combine the charts with independent y-axes
chart = alt.layer(price_line, stake_line).resolve_scale(y='independent')

# Save the combined chart
chart.save('stakingVsPriceChart.html')