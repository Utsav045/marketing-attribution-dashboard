import pandas as pd


def dataset_overview(df, dataset_name):

    print("\n" + "=" * 60)
    print(f"{dataset_name} OVERVIEW")
    print("=" * 60)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nStatistical Summary:")
    print(df.describe(include="all").transpose())


def run_eda():

    # Load datasets
    adspend_df = pd.read_csv("data/processed/adspend_featured.csv")

    interaction_df = pd.read_csv("data/processed/interaction_featured.csv")

    revenue_df = pd.read_csv("data/processed/revenue_featured.csv")

    # Dataset Overview
    dataset_overview(adspend_df, "AD SPEND DATASET")

    dataset_overview(interaction_df, "INTERACTION DATASET")

    dataset_overview(revenue_df, "REVENUE DATASET")

    # Business Insights
    print("\n" + "=" * 60)
    print("KEY BUSINESS METRICS")
    print("=" * 60)

    if "Spend" in adspend_df.columns:
        print(f"\nTotal Spend: {adspend_df['Spend'].sum():,.2f}")

    if "Revenue" in revenue_df.columns:
        print(f"Total Revenue: {revenue_df['Revenue'].sum():,.2f}")

    if "Channel" in interaction_df.columns:
        print("\nTop Channels:")
        print(interaction_df["Channel"].value_counts().head(10))

    if "User_id" in interaction_df.columns:
        print(f"\nUnique Users: {interaction_df['User_id'].nunique()}")

    # =====================================================
    # SAVE FINAL DATASETS
    # =====================================================

    adspend_df.to_csv("data/processed/eda_adspend.csv", index=False)

    interaction_df.to_csv("data/processed/eda_interaction.csv", index=False)

    revenue_df.to_csv("data/processed/eda_revenue.csv", index=False)

    print("\nEDA datasets saved successfully!")

    print("\nEDA COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    run_eda()
