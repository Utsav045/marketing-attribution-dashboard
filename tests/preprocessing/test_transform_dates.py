import pandas as pd

from src.preprocessing.transform_dates import transform_dates


def test_transform_dates_formats_date_columns():
    df = pd.DataFrame({"Date": ["2025-01-02"], "Conversion_date": ["2025-02-03"]})

    result = transform_dates(df)

    assert result.loc[0, "Date"].endswith("2025")
    assert result.loc[0, "Conversion_date"].endswith("2025")
