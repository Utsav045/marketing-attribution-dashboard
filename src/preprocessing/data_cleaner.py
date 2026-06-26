import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.drop_duplicates()

    currency_columns = [col for col in df.columns if col in {'Spend', 'Revenue'}]
    for col in currency_columns:
        df[col] = (
            df[col]
            .astype(str)
            .replace(r'[\$,]', '', regex=True)
            .replace('nan', '')
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def run_data_cleaning() -> None:
    Addspend_df = pd.read_csv('data/raw/add_spend_dataset.csv')
    interaction_df = pd.read_csv('data/raw/customer_interaction_dataset.csv')
    revenue_df = pd.read_csv('data/raw/revenue_dataset.csv')

    Addspend_df = clean_data(Addspend_df)
    interaction_df = clean_data(interaction_df)
    revenue_df = clean_data(revenue_df)

    print("\n Add Spend Dataset")
    print(Addspend_df.info())
    print("\nCustomer Interaction Dataset")
    print(interaction_df.info())
    print("\nRevenue Dataset")
    print(revenue_df.info())

    Addspend_df.to_csv(
        'data/processed/cleaned_add_spend_dataset.csv',
        index=False
    )
    interaction_df.to_csv(
        'data/processed/cleaned_customer_interaction_dataset.csv',
        index=False
    )
    revenue_df.to_csv(
        'data/processed/cleaned_revenue_dataset.csv',
        index=False
    )

    print("\nData Cleaning Completed Successfully!")


if __name__ == '__main__':
    run_data_cleaning()
