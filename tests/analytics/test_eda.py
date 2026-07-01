import pandas as pd

from src.analytics import eda


def test_eda_module_loads():
    assert eda is not None


def test_dataset_overview_prints_insights(capsys):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    eda.dataset_overview(df, "TEST DATASET")
    captured = capsys.readouterr()

    assert "TEST DATASET OVERVIEW" in captured.out
    assert "Shape:" in captured.out


def test_run_eda_writes_processed_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame({"Campaign_id": ["C1"], "Spend": [100]}).to_csv(
        processed_dir / "adspend_featured.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Campaign_id": ["C1"]}).to_csv(
        processed_dir / "interaction_featured.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Revenue": [500]}).to_csv(
        processed_dir / "revenue_featured.csv", index=False
    )

    eda.run_eda()

    assert (processed_dir / "eda_adspend.csv").exists()
    assert (processed_dir / "eda_interaction.csv").exists()
    assert (processed_dir / "eda_revenue.csv").exists()
