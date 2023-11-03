import pandas as pd
import os
import plotly.graph_objects as go
from transactions.constants import DATA_PATH, RESULTS_PATH, FIGURES_PATH

market_path = os.path.join(RESULTS_PATH, "prices", 'marketIndex.csv')
hbar_path = os.path.join(RESULTS_PATH, "prices", 'hbar_price_2023.csv')
stakes_path = os.path.join(RESULTS_PATH, "nodes", 'nodes_historical_stakes.csv')

# Load the data
market_index = pd.read_csv(market_path, parse_dates=['time'])
hbar_price = pd.read_csv(hbar_path, parse_dates=['time'])
stake_data = pd.read_csv(stakes_path, parse_dates=['time'])

# Merge the datasets on the 'time' column
merged_data = market_index.merge(hbar_price, on='time', how='outer')
merged_data = merged_data.merge(stake_data, on='time', how='outer')

# Sort by time
merged_data = merged_data.sort_values(by='time').reset_index(drop=True)

# Index the data starting from 100
for column in ['price_x', 'price_y']:
    merged_data[f"indexed_{column}"] = 100 * (merged_data[column] / merged_data[column].iloc[0])


fig = go.Figure()

# Add S&P Crypto Market Index trace
fig.add_trace(go.Scatter(x=merged_data['time'], y=merged_data['indexed_price_x'],
                         mode='lines', name='S&P Crypto Market Index', line=dict(color='red')))

# Add HBAR Price trace
fig.add_trace(go.Scatter(x=merged_data['time'], y=merged_data['indexed_price_y'],
                         mode='lines', name='HBAR Price', line=dict(color='blue')))

# Add HBAR Total Staked trace, using secondary y-axis
fig.add_trace(go.Scatter(x=merged_data['time'], y=merged_data['stake_amount'],
                         mode='lines', name='HBAR Total Staked', line=dict(color='green'), yaxis="y2"))


fig.update_layout(
    title={
        'text': "S&P Crypto Market Index & HBAR Price with Total Staked Amount",
        'font': {'size': 24, 'family': 'Courier New, monospace', 'color': 'black'}  
    },
    xaxis_title={
        'text': "Time",
        'font': {'size': 18, 'family': 'Courier New, monospace', 'color': 'black'} 
    },
    yaxis_title={
        'text': "S&P Crypto Market Index & HBAR Price",
        'font': {'size': 18, 'family': 'Courier New, monospace', 'color': 'black'} 
    },
    yaxis2=dict(
        title={
            'text': "HBAR Total Staked",
            'font': {'size': 18, 'family': 'Courier New, monospace', 'color': 'black'}  
        },
        overlaying='y',
        side='right'
    ),
    template="plotly_white"  
)

fig.show()

