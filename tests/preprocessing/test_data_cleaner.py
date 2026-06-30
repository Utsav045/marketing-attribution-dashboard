import pandas as pd

from src.preprocessing.data_cleaner import clean_data


def test_clean_data_removes_duplicates_and_converts_currency():
    df = pd.DataFrame(
        {
            "Campaign_id": ["A", "A", "B"],
            "Spend": ["$100", "$100", "$200"],
            "Revenue": ["$50", "$50", "$75"],
        }
    )

    result = clean_data(df)

    assert result.shape[0] == 2
    assert result["Spend"].tolist() == [100.0, 200.0]
