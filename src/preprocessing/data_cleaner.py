import pandas as pd

# Load datasets
Addspend_df = pd.read_csv("data/raw/Add Spend Dataset.csv")
interaction_df = pd.read_csv("data/raw/Customer Interaction Dataset.csv")
revenue_df = pd.read_csv("data/raw/Revenue Dataset.csv")

# Remove duplicates
Addspend_df = Addspend_df.drop_duplicates()
interaction_df = interaction_df.drop_duplicates()
revenue_df = revenue_df.drop_duplicates()


# Remove $ sign Add Spend Dataset
Addspend_df["Spend"] = Addspend_df["Spend"].replace(r"[\$,]", "", regex=True)

# Convert Spend to numeric
Addspend_df["Spend"] = pd.to_numeric(Addspend_df["Spend"])

# Remove $ sign Revenue Dataset
revenue_df["Revenue"] = revenue_df["Revenue"].replace(r"[\$,]", "", regex=True)

# Convert Revenue to numeric
revenue_df["Revenue"] = pd.to_numeric(revenue_df["Revenue"])



# Display dataset information
print("\n Add Spend Dataset")
print(Addspend_df.info())

print("\nCustomer Interaction Dataset")
print(interaction_df.info())

print("\nRevenue Dataset")
print(revenue_df.info())

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

print("\nData Cleaning Completed Successfully!")