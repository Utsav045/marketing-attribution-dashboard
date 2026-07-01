import pandas as pd
from src.ingestion.data_loader import load_raw_data
from src.ingestion.load_data import load_data


def test_load_data_is_callable():
    assert callable(load_data)


def test_load_raw_data_reads_expected_files(tmp_path):
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    pd.DataFrame({"A": [1]}).to_csv(raw_dir / "add_spend_dataset.csv", index=False)
    pd.DataFrame({"B": [2]}).to_csv(
        raw_dir / "customer_interaction_dataset.csv", index=False
    )
    pd.DataFrame({"C": [3]}).to_csv(raw_dir / "revenue_dataset.csv", index=False)

    datasets = load_raw_data(root_dir=tmp_path)

    assert datasets["add_spend"].iloc[0, 0] == 1
    assert datasets["customer_interaction"].iloc[0, 0] == 2
    assert datasets["revenue"].iloc[0, 0] == 3
