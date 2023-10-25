import pandas as pd
import altair as alt
from transactions.constants import DATA_PATH, RESULTS_PATH, FIGURES_PATH

# Load the data
file_path = os.path.join(RESULTS_PATH, "hourly_average_fees_USD.csv")
df = pd.read_csv(file_path)

# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'])

# Create the chart
base = alt.Chart(df).encode(
    x=alt.X('time:T', title='Time', axis=alt.Axis(grid=False)),
    y=alt.Y('fee_USD:Q', title='Fee (USD)', axis=alt.Axis(grid=True))
)

line = base.mark_line(color='blue', strokeWidth=2).encode(
    tooltip=['time:T', 'fee_USD:Q']
)

threshold = alt.Chart(df).mark_rule(color='red', strokeWidth=1).encode(
    y='a:Q'
).transform_calculate(
    a="0.0001"
)

chart = (line + threshold).properties(
    title='Average Fees Over Time',
    width=800,
    height=400
).configure_view(
    strokeWidth=0
).configure_title(
    fontSize=20,
    anchor='middle'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)

# Save the chart
chart.save(os.path.join(FIGURES_PATH, 'avg_fees_in_usd.html'))

# Display the chart
chart.display()
