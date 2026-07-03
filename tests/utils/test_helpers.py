import pandas as pd

from src.utils.helpers import (
    check_duplicates,
    check_missing_values,
    generate_summary,
    load_csv,
    save_csv,
)


def test_check_missing_values_reports_missing_values():
    df = pd.DataFrame({"A": [1, None], "B": [2, 3]})

    result = check_missing_values(df)

    assert result["A"] == 1
    assert result["B"] == 0


def test_load_and_save_csv(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    path = tmp_path / "sample.csv"

    save_csv(df, path)
    loaded = load_csv(path)

    assert loaded is not None
    assert list(loaded.columns) == ["A", "B"]
    assert loaded.iloc[0, 0] == 1


def test_check_duplicates_reports_duplicate_rows():
    df = pd.DataFrame({"A": [1, 1, 2]})

    assert check_duplicates(df) == 1


def test_generate_summary_returns_dataframe():
    df = pd.DataFrame({"A": [1, 2, 3]})

    summary = generate_summary(df)

    assert "A" in summary.columns
    assert summary.loc["mean", "A"] == 2.0
