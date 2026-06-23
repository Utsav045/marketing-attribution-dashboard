import pandas as pd

Addspend_df = pd.read_csv("data/raw/add_spend_dataset.csv")
interaction_df = pd.read_csv("data/raw/customer_interaction_dataset.csv")
revenue_df = pd.read_csv("data/raw/revenue_dataset.csv")

print(Addspend_df.head())
print(interaction_df.head())
print(revenue_df.head())