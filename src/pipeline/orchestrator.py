import pandas as pd

from src.preprocessing.data_cleaner import clean_data
from src.preprocessing.handle_missing import handle_missing
from src.preprocessing.transform_dates import convert_date
from src.preprocessing.transform_dates import transform_dates
from src.preprocessing.feature_engineering import feature_engineering


def run_pipeline():

    print("=" * 50)
    print("STARTING DATA PIPELINE")
    print("=" * 50)

    # =====================================================
    # LOAD DATASETS
    # =====================================================

    adspend_df = pd.read_csv(
        "data/raw/Add Spend Dataset.csv"
    )

    interaction_df = pd.read_csv(
        "data/raw/Customer Interaction Dataset.csv"
    )

    revenue_df = pd.read_csv(
        "data/raw/Revenue Dataset.csv"
    )

    print("Datasets Loaded Successfully")

    # =====================================================
    # DATA CLEANING
    # =====================================================

    adspend_df = clean_data(adspend_df)
    interaction_df = clean_data(interaction_df)
    revenue_df = clean_data(revenue_df)

    print("Data Cleaning Completed")

    # =====================================================
    # HANDLE MISSING VALUES
    # =====================================================

    adspend_df = handle_missing(adspend_df)
    interaction_df = handle_missing(interaction_df)
    revenue_df = handle_missing(revenue_df)

    print("Missing Value Handling Completed")

    # =====================================================
    # DATE CONVERSION
    # =====================================================

    adspend_df = transform_dates(adspend_df)
    interaction_df = transform_dates(interaction_df)
    revenue_df = transform_dates(revenue_df)
    print("Date Transformation Completed")

    # =====================================================
    # FEATURE ENGINEERING
    # =====================================================

    (
        adspend_df,
        interaction_df,
        revenue_df
    ) = feature_engineering(
        adspend_df,
        interaction_df,
        revenue_df
    )

    print("Feature Engineering Completed")

    # =====================================================
    # SAVE FINAL DATASETS
    # =====================================================

    adspend_df.to_csv(
        "data/processed/adspend_featured.csv",
        index=False
    )

    interaction_df.to_csv(
        "data/processed/interaction_featured.csv",
        index=False
    )

    revenue_df.to_csv(
        "data/processed/revenue_featured.csv",
        index=False
    )

    print("\nProcessed Datasets Saved")

    print("\nGenerated Files:")
    print("data/processed/adspend_featured.csv")
    print("data/processed/interaction_featured.csv")
    print("data/processed/revenue_featured.csv")

    print("\nPIPELINE COMPLETED SUCCESSFULLY")

    return (
        adspend_df,
        interaction_df,
        revenue_df
    )