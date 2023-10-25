import pandas as pd
import plotly.graph_objects as go
import os
import random
from os import path
from transactions.constants import DATA_PATH, RESULTS_PATH, FIGURES_PATH

# Load the data
file_path = os.path.join(RESULTS_PATH, "hourly_average_fees_by_type.csv")
df = pd.read_csv(file_path)

# Convert 'hour' 
df['time'] = pd.to_datetime(df['time'])

colors = {'CRYPTOAPPROVEALLOWANCE': '#C5DAEF',
          'CRYPTOTRANSFER': '#92B2D5',
          'CONSENSUSSUBMITMESSAGE': '#F0D9AB',
          'CONTRACTCALL': '#E3AFC4',
          'CRYPTOCREATEACCOUNT': '#EFC6AE',
          'CRYPTOUPDATEACCOUNT': '#7BB3AF',
          'FILEUPDATE':'#92B2D5',
          'TOKENMINT':'#7AB47E',
          'TOKENBURN':'#808DDE'
          }

# Create a list of traces for each transaction type
traces = []
for col in ['CONSENSUSSUBMITMESSAGE', 'CRYPTOAPPROVEALLOWANCE', 'CONTRACTCALL', 'CRYPTOCREATEACCOUNT', 'CRYPTOTRANSFER','CRYPTOUPDATEACCOUNT', 'FILEUPDATE', 'TOKENMINT', 'TOKENBURN']:
    traces.append(go.Scatter(x=df['time'], y=df[col], fill='tonexty',
                             mode='none', name=col, fillcolor=colors[col], stackgroup='one'))

fig = go.Figure(data=traces)

# Update the layout
fig.update_layout(title={'text': 'Transaction Fees by Type Over Time',
                         'y':0.98,
                         'x':0.5,
                         'xanchor': 'center',
                         'yanchor': 'top'},
                  xaxis_title='Time',
                  yaxis_title='Average Transaction Fees',
                  legend_title='Hedera Transaction Types',
                  hovermode='x unified',
                  margin=dict(l=50, r=50, b=50, t=50, pad=4),
                  plot_bgcolor='white',
                  paper_bgcolor='white',
                  font=dict(size=12, color='#7f7f7f'),
                  xaxis=dict(showgrid=False,
                             tickformat='%Y-%m-%d',
                             tickmode='array',
                             tickvals=df['time'].tolist()[::len(df['time'])//10],
                             rangeselector=dict(
                                 buttons=list([
                                     dict(count=7, label="1w", step="day", stepmode="backward"),
                                     dict(count=1, label="1m", step="month", stepmode="backward"),
                                     dict(count=6, label="6m", step="month", stepmode="backward"),
                                     dict(count=1, label="1y", step="year", stepmode="backward"),
                                     dict(step="all")
                                 ])
                             ),
                             rangeslider=dict(visible=True),
                             type="date"
                            ),
                  yaxis=dict(showgrid=False))  # Removed tickformat here

# Update the legend
fig.update_layout(legend=dict(orientation='h',
                              y=-0.7,
                              x=0.5,
                              xanchor='center'))

# Save the figure as an HTML file
fig.write_html(path.join(FIGURES_PATH, "transaction_fees_by_type_over_time.html"))

# Show the chart
fig.show()