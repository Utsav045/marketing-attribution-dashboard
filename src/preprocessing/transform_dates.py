import pandas as pd


def convert_date(date_col: pd.Series) -> pd.Series:
    """
    Convert date column into DD/MM/YYYY format.
    """

    return pd.to_datetime(
        date_col,
        errors="coerce"
    ).dt.strftime("%d/%m/%Y")


def transform_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform all date columns in a dataframe.
    """

    df = df.copy()

    df.columns = df.columns.str.strip()

    if "Date" in df.columns:
        df["Date"] = convert_date(df["Date"])

    if "Interaction_date" in df.columns:
        df["Interaction_date"] = convert_date(
            df["Interaction_date"]
        )

    if "Conversion_date" in df.columns:
        df["Conversion_date"] = convert_date(
            df["Conversion_date"]
        )

    return df


def run_transform_dates():

    print("Starting Date Transformation...")

    adspend_df = pd.read_csv(
        "data/processed/cleaned_add_spend_dataset.csv"
    )

    interaction_df = pd.read_csv(
        "data/processed/cleaned_customer_interaction_dataset.csv"
    )

    revenue_df = pd.read_csv(
        "data/processed/cleaned_revenue_dataset.csv"
    )

    adspend_df = transform_dates(adspend_df)
    interaction_df = transform_dates(interaction_df)
    revenue_df = transform_dates(revenue_df)

    adspend_df.to_csv(
        "data/processed/cleaned_add_spend_dataset.csv",
        index=False
    )

    interaction_df.to_csv(
        "data/processed/cleaned_customer_interaction_dataset.csv",
        index=False
    )

    revenue_df.to_csv(
        "data/processed/cleaned_revenue_dataset.csv",
        index=False
    )

    print("Date Transformation Completed Successfully")


if __name__ == "__main__":
    run_transform_dates()