import pandas as pd

from src.preprocessing.data_cleaner import clean_data
from src.preprocessing.feature_engineering import feature_engineering
from src.preprocessing.handle_missing import handle_missing
from src.preprocessing.transform_dates import transform_dates


def test_clean_data_removes_duplicates_and_converts_currency():
    df = pd.DataFrame({
        "Campaign_id": ["C1", "C1"],
        "Spend": ["$1000", "$1000"],
        "Revenue": ["$500", "$500"],
    })

    result = clean_data(df)

    assert result.shape[0] == 1
    assert result.loc[0, "Spend"] == 1000
    assert result.loc[0, "Revenue"] == 500


def test_handle_missing_fills_unknown_values():
    df = pd.DataFrame({
        "Campaign_id": ["C1", None],
        "Spend": [1000, None],
    })

    result = handle_missing(df)

    assert result.loc[1, "Campaign_id"] == "Unknown"
    assert result.loc[1, "Spend"] == "Unknown"


def test_transform_dates_formats_date_columns():
    df = pd.DataFrame({
        "Date": ["2025-01-01", "01/02/2025"],
        "Conversion_date": ["2025-03-01", ""],
    })

    result = transform_dates(df)

    assert result.loc[0, "Date"] == "01/01/2025"
    assert result.loc[1, "Date"] == "02/01/2025"
    assert result.loc[0, "Conversion_date"] == "01/03/2025"
    assert result.loc[1, "Conversion_date"] == "NaT"


def test_feature_engineering_adds_expected_features():
    adspend_df = pd.DataFrame({
        "Impressions": [10000, 0],
        "Clicks": [100, 0],
        "Spend": [1000, 0],
    })
    interaction_df = pd.DataFrame({
        "Impressions": [100, 50],
        "Clicks": [10, 5],
        "Spend": [100, 50],
    })
    revenue_df = pd.DataFrame({
        "Revenue": [50, 500],
    })

    adspend_result, interaction_result, revenue_result = feature_engineering(
        adspend_df,
        interaction_df,
        revenue_df,
    )

    assert "CTR" in adspend_result.columns
    assert "CPC" in adspend_result.columns
    assert "Revenue_Log" in revenue_result.columns
    assert revenue_result.loc[1, "High_Value_Conversion"] == 1
