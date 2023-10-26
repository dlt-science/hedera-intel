import pandas as pd
import os
import plotly.graph_objects as go
from transactions.constants import DATA_PATH, RESULTS_PATH, FIGURES_PATH

# Paths to the CSV files
prices_path = os.path.join(RESULTS_PATH, "hbar_prices", "hbar_price_JulyOct2023.csv")
stakes_path = os.path.join(RESULTS_PATH, "nodes", "nodes_historical_stakes.csv")

# Load the CSV files into pandas DataFrames
df_prices = pd.read_csv(prices_path)
df_stakes = pd.read_csv(stakes_path)

# Convert the "time" columns to a common datetime format
df_prices["time"] = pd.to_datetime(df_prices["time"])
df_stakes["time"] = pd.to_datetime(df_stakes["time"])

# Merge the two DataFrames on the standardized "time" column
df = pd.merge(df_prices, df_stakes, on="time")

# Normalize the date format
df['time'] = df['time'].dt.strftime('%b %d, %Y')

fig = go.Figure()

# Creating first trace
fig.add_trace(go.Scatter(x=df['time'], y=df['price'],
                         mode='lines',
                         name='HBAR Price (from CoinMetrics)'))

# Creating second trace, with secondary y-axis
fig.add_trace(go.Scatter(x=df['time'], y=df['stake_amount'],
                         mode='lines',
                         name='HBAR Total Staked',
                         yaxis="y2"))

# Add a vertical line at August 11, 2023
fig.add_vline(x='Aug 11, 2023', line_dash="dash", line_color="red")

# Updating layout to include 2 y-axes, one on the left (y1) and one on the right (y2)
fig.update_layout(
    title='HBAR Price and Total Amount Staked Over Time (Aug 11, 2023: Staking reward rate reduced from 6.5% to 2.5%)',
    xaxis_title='Time',
    yaxis=dict(
        title='HBAR Price',
    ),
    yaxis2=dict(
        title='HBAR Total Staked',
        anchor="free",
        overlaying="y",
        side="right",
        position=1
    )
)

# Save the figure as an HTML file
fig.write_html(os.path.join(FIGURES_PATH, "StakingVsPrice.html"))

fig.show()

