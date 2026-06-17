import pandas as pd

# Load datasets
interaction_df = pd.read_csv(
    "data/processed/cleaned Customer Interaction Dataset.csv"
)

Addspend_df = pd.read_csv(
    "data/processed/cleaned Add Spend Dataset.csv"
)

revenue_df = pd.read_csv(
    "data/processed/cleaned Revenue Dataset.csv"
)

# Remove spaces from column names
interaction_df.columns = interaction_df.columns.str.strip()
Addspend_df.columns = Addspend_df.columns.str.strip()
revenue_df.columns = revenue_df.columns.str.strip()

# Function to convert mixed date formats
def convert_date(date_col):
    return (
        pd.to_datetime(
            date_col,
            format="mixed",
            dayfirst=False,
            errors="coerce"
        )
        .dt.strftime("%d/%m/%Y")
    )

# Convert dates
interaction_df["Interaction_date"] = convert_date(
    interaction_df["Interaction_date"]
)

Addspend_df["Date"] = convert_date(
    Addspend_df["Date"]
)

revenue_df["Conversion_date"] = convert_date(
    revenue_df["Conversion_date"]
)

# Save datasets
interaction_df.to_csv(
    "data/processed/cleaned Customer Interaction Dataset.csv",
    index=False
)

Addspend_df.to_csv(
    "data/processed/cleaned Add Spend Dataset.csv",
    index=False
)

revenue_df.to_csv(
    "data/processed/cleaned Revenue Dataset.csv",
    index=False
)

print("All dates converted successfully!")