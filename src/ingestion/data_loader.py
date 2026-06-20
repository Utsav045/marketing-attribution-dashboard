import pandas as pd

Addspend_df = pd.read_csv("data/raw/Add_Spend_Dataset.csv")
interaction_df = pd.read_csv("data/raw/Customer_Interaction_dataset.csv")
revenue_df = pd.read_csv("data/raw/Revenue_dataset.csv")

print(Addspend_df.head())
print(interaction_df.head())
print(revenue_df.head())