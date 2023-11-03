import pandas as pd
import altair as alt

# Data for the charts
total_transactions =  33727851
transactions_with_memo = 6924487
scam_messages = 276311
transactions_without_memo = total_transactions - transactions_with_memo
legitimate_memos = transactions_with_memo - scam_messages

# Calculate percentages
scam_messages_percentage = (scam_messages / transactions_with_memo) * 100
legitimate_memos_percentage = 100 - scam_messages_percentage

memo_transactions_percentage = (transactions_with_memo / total_transactions) * 100
no_memo_percentage = 100 - memo_transactions_percentage

# First pie chart data: Scam messages vs. legitimate memos
source1 = pd.DataFrame({
    "category": ['Scam Messages', 'Legitimate Memos'],
    "value": [scam_messages, legitimate_memos],
    "percentage": [scam_messages_percentage, legitimate_memos_percentage]
})

# Second pie chart data: Transactions with memos vs. no memos
source2 = pd.DataFrame({
    "category": ['Transactions with Memo', 'No Memo'],
    "value": [transactions_with_memo, transactions_without_memo],
    "percentage": [memo_transactions_percentage, no_memo_percentage]
})

# Creating the first pie chart
chart1 = alt.Chart(source1).mark_arc().encode(
    theta='value:Q',
    color='category:N',
    tooltip=['category:N', 'value:Q', 'percentage:Q']
).properties(
    width=400,
    height=400,
    title="Memo Transaction Distribution"
)

# Creating the second pie chart
chart2 = alt.Chart(source2).mark_arc().encode(
    theta='value:Q',
    color='category:N',
    tooltip=['category:N', 'value:Q', 'percentage:Q']
).properties(
    width=400,
    height=400,
    title="Overall Transaction Distribution"
)

# Save both charts as HTML files
chart1.save('MemoTransactionDistribution.html')
chart2.save('OverallTransactionDistribution.html')
