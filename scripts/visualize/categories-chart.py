import pandas as pd
import matplotlib.pyplot as plt
import os
from transactions.constants import RESULTS_PATH
from transactions.constants import FIGURES_PATH

df = pd.read_csv(os.path.join(RESULTS_PATH, 'transaction_categories.csv'))

df = df[df['Category'] != 'Total']

# Group by 'Category' and sum the percentages
category_percentages = df.groupby('Category')['Percentage'].sum()

# Filter categories and combine small categories into 'Others'
threshold = 1  
small_categories = category_percentages[category_percentages < threshold]
category_percentages = category_percentages[category_percentages >= threshold]
category_percentages['Others'] = small_categories.sum()

colors = plt.cm.Paired(range(len(category_percentages)))

# Plot a pie chart
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(category_percentages, labels=category_percentages.index, 
                                  autopct='%1.1f%%', startangle=90, colors=colors, 
                                  shadow=False, textprops=dict(color="w", weight="bold", size=12))

ax.axis('equal')  

plt.title('Hedera Transactions by Category', y=1.1, fontweight='bold', fontsize=16)

# Add a legend
legend = ax.legend(wedges, category_percentages.index, title="Categories", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1))
plt.setp(legend.get_title(), fontweight='bold')

# Explanation of 'Others'
explanation = f"Others include: {', '.join(small_categories.index)}"
plt.annotate(explanation, xy=(0, 0), xytext=(0, -180), textcoords='offset points', fontsize=9, ha='center')

for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_color('white')

plt.savefig(os.path.join(FIGURES_PATH, 'transaction_categories.pdf'), bbox_inches='tight')

plt.show()

