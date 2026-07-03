import pandas as pd

from src.preprocessing.handle_missing import handle_missing


def test_handle_missing_replaces_nans_with_unknown():
    df = pd.DataFrame({"Campaign_id": ["A", None], "Spend": [100, None]})

    result = handle_missing(df)

    assert result.loc[1, "Campaign_id"] == "Unknown"
    assert result.loc[1, "Spend"] == "Unknown"


def test_run_handle_missing_writes_cleaned_files(tmp_path, monkeypatch):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    pd.DataFrame({"Campaign_id": ["A", None], "Spend": [100, None]}).to_csv(
        raw_dir / "add_spend_dataset.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Campaign_id": ["A"]}).to_csv(
        raw_dir / "customer_interaction_dataset.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Revenue": ["$200"]}).to_csv(
        raw_dir / "revenue_dataset.csv", index=False
    )

    monkeypatch.chdir(tmp_path)
    from src.preprocessing.handle_missing import run_handle_missing

    run_handle_missing()

    assert (tmp_path / "data" / "processed" / "cleaned_add_spend_dataset.csv").exists()
    assert (
        tmp_path / "data" / "processed" / "cleaned_customer_interaction_dataset.csv"
    ).exists()
    assert (tmp_path / "data" / "processed" / "cleaned_revenue_dataset.csv").exists()
