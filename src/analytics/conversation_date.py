import pandas as pd


def conversion_date_analysis():

    # ==========================================
    # LOAD DATASET
    # ==========================================

    revenue_df = pd.read_csv(
        "data/processed/revenue_featured.csv"
    )

    # ==========================================
    # CONVERT DATE COLUMN
    # ==========================================

    revenue_df["Conversion_date"] = pd.to_datetime(
        revenue_df["Conversion_date"],
        dayfirst=True,
        errors="coerce"
    )

    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================

    revenue_df["Conversion_Year"] = (
        revenue_df["Conversion_date"].dt.year
    )

    revenue_df["Conversion_Month"] = (
        revenue_df["Conversion_date"].dt.month_name()
    )

    revenue_df["Conversion_Weekday"] = (
        revenue_df["Conversion_date"].dt.day_name()
    )

    revenue_df["Conversion_Quarter"] = (
        revenue_df["Conversion_date"].dt.quarter
    )

    revenue_df["Conversion_Day"] = (
        revenue_df["Conversion_date"].dt.day
    )

    # ==========================================
    # PRINT ANALYSIS
    # ==========================================

    print("\n" + "=" * 60)
    print("CONVERSION DATE ANALYSIS")
    print("=" * 60)

    print("\nDataset Shape:")
    print(revenue_df.shape)

    print("\nColumns:")
    print(revenue_df.columns.tolist())

    print("\nData Types:")
    print(revenue_df.dtypes)

    print("\nMissing Values:")
    print(revenue_df.isnull().sum())

    print("\nFirst 5 Rows:")
    print(revenue_df.head())

    print("\nTotal Revenue:")
    print(revenue_df["Revenue"].sum())

    print("\nMonthly Conversions:")
    print(
        revenue_df["Conversion_Month"]
        .value_counts()
        .sort_index()
    )

    print("\nWeekday Conversions:")
    print(
        revenue_df["Conversion_Weekday"]
        .value_counts()
    )

    print("\nQuarterly Conversions:")
    print(
        revenue_df["Conversion_Quarter"]
        .value_counts()
        .sort_index()
    )

    print("\nYearly Conversions:")
    print(
        revenue_df["Conversion_Year"]
        .value_counts()
        .sort_index()
    )

    # ==========================================
    # SAVE FINAL DATASET
    # ==========================================

    revenue_df.to_csv(
        "data/processed/conversion_date_analysis.csv",
        index=False
    )

    print(
        "\nSaved to: data/processed/conversion_date_analysis.csv"
    )

    print("\nCONVERSION DATE ANALYSIS COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    conversion_date_analysis()