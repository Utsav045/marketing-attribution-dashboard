import pandas as pd

# Load datasets
customer_df = pd.read_csv("data/raw/Add Spend Dataset.csv")
interaction_df = pd.read_csv("data/raw/Customer Interaction Dataset.csv")
revenue_df = pd.read_csv("data/raw/Revenue Dataset.csv")

# Remove duplicates
customer_df = customer_df.drop_duplicates()
interaction_df = interaction_df.drop_duplicates()
revenue_df = revenue_df.drop_duplicates()


# Remove $ sign Add Spend Dataset
customer_df["Spend"] = customer_df["Spend"].replace(r"[\$,]", "", regex=True)

# Convert Spend to numeric
customer_df["Spend"] = pd.to_numeric(customer_df["Spend"])

# Remove $ sign Revenue Dataset
revenue_df["Revenue"] = revenue_df["Revenue"].replace(r"[\$,]", "", regex=True)

# Convert Revenue to numeric
revenue_df["Revenue"] = pd.to_numeric(revenue_df["Revenue"])



# Display dataset information
print("\n Add Spend Dataset")
print(customer_df.info())

print("\nCustomer Interaction Dataset")
print(interaction_df.info())

print("\nRevenue Dataset")
print(revenue_df.info())

# Save cleaned datasets
customer_df.to_csv(
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