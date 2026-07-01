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
    assert result["Revenue"].tolist() == [50.0, 75.0]


def test_clean_data_handles_non_numeric_currency_values():
    df = pd.DataFrame({"Spend": ["$100", "invalid"], "Revenue": ["$50", "$75"]})

    result = clean_data(df)

    assert result.loc[1, "Spend"] != "invalid"
    assert pd.isna(result.loc[1, "Spend"])


def test_run_data_cleaning_writes_files(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    pd.DataFrame({"Campaign_id": ["A"], "Spend": ["$100"], "Revenue": ["$50"]}).to_csv(
        raw_dir / "add_spend_dataset.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Campaign_id": ["A"]}).to_csv(
        raw_dir / "customer_interaction_dataset.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Revenue": ["$200"]}).to_csv(
        raw_dir / "revenue_dataset.csv", index=False
    )

    monkeypatch.chdir(tmp_path)
    from src.preprocessing.data_cleaner import run_data_cleaning

    run_data_cleaning()

    assert (tmp_path / "data" / "processed" / "cleaned_add_spend_dataset.csv").exists()
    assert (
        tmp_path / "data" / "processed" / "cleaned_customer_interaction_dataset.csv"
    ).exists()
    assert (tmp_path / "data" / "processed" / "cleaned_revenue_dataset.csv").exists()
