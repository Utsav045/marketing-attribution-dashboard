import pandas as pd

from src.preprocessing.handle_missing import handle_missing


def test_handle_missing_replaces_nans_with_unknown():
    df = pd.DataFrame({"Campaign_id": ["A", None], "Spend": [100, None]})

    result = handle_missing(df)

    assert result.loc[1, "Campaign_id"] == "Unknown"
    assert result.loc[1, "Spend"] is None or result.loc[1, "Spend"] == "Unknown"
