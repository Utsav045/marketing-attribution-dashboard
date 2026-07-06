import pandas as pd

from src.preprocessing.data_cleaner import clean_data
from src.preprocessing.feature_engineering import feature_engineering
from src.preprocessing.handle_missing import handle_missing
from src.preprocessing.transform_dates import transform_dates

sample_df = pd.DataFrame(
    {
        "Campaign_id": ["C1", "C2"],
        "Spend": [1000, 2000],
        "Clicks": [100, 200],
        "Impressions": [10000, 20000],
        "Date": ["2025-01-01", "2025-01-02"],
    }
)


def test_clean_data_import_and_run():
    cleaned = clean_data(sample_df.copy())
    assert cleaned is not None
    assert "Campaign_id" in cleaned.columns


def test_handle_missing_import_and_run():
    handled = handle_missing(sample_df.copy())
    assert handled is not None
    assert handled.isnull().sum().sum() == 0


def test_transform_dates_import_and_run():
    transformed = transform_dates(sample_df.copy())
    assert "Date" in transformed.columns
    assert transformed.loc[0, "Date"].endswith("2025")


def test_feature_engineering_import_and_run():
    sample_interaction = pd.DataFrame(
        {"Interaction_date": ["2025-01-01", "2025-01-02"]}
    )
    sample_revenue = pd.DataFrame({"Revenue": [100, 200]})

    result_adspend, result_interaction, result_revenue = feature_engineering(
        sample_df.copy(), sample_interaction, sample_revenue
    )

    assert result_adspend is not None
    assert result_interaction is not None
    assert result_revenue is not None
    assert "CTR" in result_adspend.columns
    assert "Interaction_Day" in result_interaction.columns
    assert "Revenue_Category" in result_revenue.columns
