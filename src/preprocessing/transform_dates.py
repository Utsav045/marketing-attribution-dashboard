import pandas as pd


def convert_date(date_col: pd.Series) -> pd.Series:
    return (
        pd.to_datetime(
            date_col,
            dayfirst=False,
            errors='coerce'
        )
        .dt.strftime('%d/%m/%Y')
    )


def transform_dates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip()

    if 'Interaction_date' in df.columns:
        df['Interaction_date'] = convert_date(df['Interaction_date'])
    if 'Date' in df.columns:
        df['Date'] = convert_date(df['Date'])
    if 'Conversion_date' in df.columns:
        df['Conversion_date'] = convert_date(df['Conversion_date'])

    return df


def run_transform_dates() -> None:
    interaction_df = pd.read_csv('data/processed/cleaned_customer_interaction_dataset.csv')
    Addspend_df = pd.read_csv('data/processed/cleaned_add_spend_dataset.csv')
    revenue_df = pd.read_csv('data/processed/cleaned_revenue_dataset.csv')

    interaction_df = transform_dates(interaction_df)
    Addspend_df = transform_dates(Addspend_df)
    revenue_df = transform_dates(revenue_df)

    interaction_df.to_csv(
        'data/processed/cleaned_customer_interaction_dataset.csv',
        index=False
    )
    Addspend_df.to_csv(
        'data/processed/cleaned_add_spend_dataset.csv',
        index=False
    )
    revenue_df.to_csv(
        'data/processed/cleaned_revenue_dataset.csv',
        index=False
    )

    print('All dates converted successfully!')


if __name__ == '__main__':
    run_transform_dates()
