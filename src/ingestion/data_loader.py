import pandas as pd

customer_df = pd.read_csv("data/raw/Add Spend Dataset.csv")
interaction_df = pd.read_csv("data/raw/Customer Interaction Dataset.csv")
revenue_df = pd.read_csv("data/raw/Revenue Dataset.csv")

print(customer_df.head())
print(interaction_df.head())
print(revenue_df.head())