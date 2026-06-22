import pandas as pd

from src.utils.file_manager import create_directory, delete_file
from src.utils.helpers import check_duplicates, check_missing_values, generate_summary


def test_check_missing_values_counts_nulls_correctly():
    df = pd.DataFrame({"A": [1, None, 2], "B": [None, 2, 3]})
    result = check_missing_values(df)

    assert result["A"] == 1
    assert result["B"] == 1


def test_check_duplicates_counts_duplicate_rows():
    df = pd.DataFrame({"A": [1, 1], "B": [2, 2]})
    assert check_duplicates(df) == 1


def test_generate_summary_returns_dataframe():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    summary = generate_summary(df)

    assert summary.loc["mean", "A"] == 2
    assert summary.loc["mean", "B"] == 5


def test_file_manager_create_directory(tmp_path):
    target = tmp_path / "test_dir"
    created = create_directory(target)

    assert created.exists()
    assert created.is_dir()
