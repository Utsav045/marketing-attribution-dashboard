import pandas as pd

from src.utils.helpers import check_missing_values


def test_check_missing_values_reports_missing_values():
    df = pd.DataFrame({"A": [1, None], "B": [2, 3]})

    result = check_missing_values(df)

    assert result["A"] == 1
    assert result["B"] == 0
