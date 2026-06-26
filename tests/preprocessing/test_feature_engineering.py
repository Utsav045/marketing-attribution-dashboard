import pandas as pd

from src.preprocessing.feature_engineering import feature_engineering


def test_feature_engineering_adds_expected_columns():
    adspend_df = pd.DataFrame({"Impressions": [100], "Clicks": [10], "Spend": [100]})
    interaction_df = pd.DataFrame({"Impressions": [100], "Clicks": [10], "Spend": [100]})
    revenue_df = pd.DataFrame({"Revenue": [100]})

    result_adspend, result_interaction, result_revenue = feature_engineering(adspend_df, interaction_df, revenue_df)

    assert "CTR" in result_adspend.columns
    assert "Interaction_Rate" in result_interaction.columns
    assert "Revenue_Log" in result_revenue.columns
