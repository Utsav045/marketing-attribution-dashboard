import pandas as pd

# Load datasets
Addspend_df = pd.read_csv("data/raw/Add Spend Dataset.csv")
interaction_df = pd.read_csv("data/raw/Customer Interaction Dataset.csv")
revenue_df = pd.read_csv("data/raw/Revenue Dataset.csv")


# Handle missing values
Addspend_df = Addspend_df.fillna("Unknown")
interaction_df = interaction_df.fillna(0)
revenue_df = revenue_df.fillna(0)


# Save cleaned datasets
Addspend_df.to_csv(
    "data/processed/cleaned Add Spend Dataset.csv",
    index=False
)

interaction_df.to_csv(
    "data/processed/cleaned Customer Interaction Dataset.csv",
    index=False
)

revenue_df.to_csv(
    "data/processed/cleaned Revenue Dataset.csv",
    index=False
)

print("\n Missing Value Handling Completed Successfully!")