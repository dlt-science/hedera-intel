import pandas as pd
import os
from transactions.constants import RESULTS_PATH

df = pd.read_csv(os.path.join(RESULTS_PATH, 'transaction_types.csv'))

# Categories dictionary
categories = {
    "Account Actions": ["CRYPTOCREATEACCOUNT", "CRYPTOUPDATEACCOUNT", "CRYPTOAPPROVEALLOWANCE",
                        "CRYPTODELETEALLOWANCE", "CRYPTODELETE", "FREEZE"],
    "Transfers": ["CRYPTOTRANSFER"],
    "Consensus": ["CONSENSUSSUBMITMESSAGE", "CONSENSUSCREATETOPIC"],
    "Smart Contracts": ["CONTRACTCALL", "CONTRACTCREATEINSTANCE", "SCHEDULECREATE", "SCHEDULESIGN"],
    "File Service": ["FILEUPDATE", "FILECREATE", "FILEAPPEND"],
    "Tokens": ["TOKENMINT", "TOKENBURN", "TOKENFREEZE", "TOKENASSOCIATE", 
               "TOKENDISSOCIATE", "TOKENCREATION", "TOKENGRANTKYC", "UTILPRNG"]
}

# Function to assign categories
def assign_category(transaction_type):
    for category, types in categories.items():
        if transaction_type in types:
            return category
    return "Others"

df['Category'] = df['Transaction type'].apply(assign_category)

cols = ['Category'] + [col for col in df if col != 'Category']
df = df[cols]


df = df.sort_values(by='Category', ascending=False)

df['Percentage'] = df['Percentage'].apply(lambda x: round(x, 3))
total_count = df['Count'].sum()
total_percentage = df['Percentage'].sum()

df.loc[len(df.index)] = ['Total', '', total_count, round(total_percentage)]


df.to_csv(os.path.join(RESULTS_PATH, 'transaction_categories.csv'), index=False)

print(df)
