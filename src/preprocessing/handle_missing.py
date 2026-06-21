import pandas as pd


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    return df.fillna('Unknown')


def run_handle_missing() -> None:
    Addspend_df = pd.read_csv('data/raw/add_spend_dataset.csv')
    interaction_df = pd.read_csv('data/raw/customer_interaction_dataset.csv')
    revenue_df = pd.read_csv('data/raw/revenue_dataset.csv')

    Addspend_df = handle_missing(Addspend_df)
    interaction_df = handle_missing(interaction_df)
    revenue_df = handle_missing(revenue_df)

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

    print("\n Missing Value Handling Completed Successfully")


if __name__ == '__main__':
    run_handle_missing()
