import pandas as pd

# Load datasets
Addspend_df = pd.read_csv("data/raw/Add Spend Dataset.csv")
interaction_df = pd.read_csv("data/raw/Customer Interaction Dataset.csv")
revenue_df = pd.read_csv("data/raw/Revenue Dataset.csv")


# Convert date columns
Addspend_df["Date"] = pd.to_datetime(
    Addspend_df["Date"]
)

interaction_df["Interaction_date"] = pd.to_datetime(
    interaction_df["Interaction_date"]
)

revenue_df["Conversion_date"] = pd.to_datetime(
    revenue_df["Conversion_date"]
)



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

print("\n Dates Transformation Completed Successfully!")