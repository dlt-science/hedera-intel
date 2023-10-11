import pandas as pd
import os
from transactions.constants import RESULTS_PATH



df = pd.read_csv(os.path.join(RESULTS_PATH, 'transaction_types.csv'))

# Categories dictionary
categories = {
    "Accounts Actions": ["CRYPTOCREATEACCOUNT", "CRYPTOUPDATEACCOUNT", "CRYPTOAPPROVEALLOWANCE", 
                         "CRYPTODELETEALLOWANCE", "CRYPTODELETE"],
    "Transfers": ["CRYPTOTRANSFER"],
    "Consensus": ["CONSENSUSSUBMITMESSAGE", "CONSENSUSCREATETOPIC"],
    "Smart Contracts": ["CONTRACTCALL", "CONTRACTCREATEINSTANCE", "SCHEDULECREATE", "SCHEDULESIGN"],
    "File Service": ["FILEUPDATE", "FILECREATE", "FILEAPPEND"],
    "Tokens": ["TOKENMINT", "TOKENBURN", "TOKENFREEZE", "TOKENASSOCIATE", 
               "TOKENDISSOCIATE", "TOKENCREATION", "TOKENGRANTKYC", "FREEZE", "UTILPRNG"]
}

def assign_category(transaction_type):
    for category, types in categories.items():
        if transaction_type in types:
            return category
    return "Others"


df['Category'] = df['Transaction type'].apply(assign_category)


cols = ['Category'] + [col for col in df if col != 'Category']
df = df[cols]

df = df.sort_values(by='Category', ascending=False)

df.to_csv(os.path.join(RESULTS_PATH, 'transactions_categories.csv'), index=False)

print(df)