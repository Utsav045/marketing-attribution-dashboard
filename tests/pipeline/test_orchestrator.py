import pandas as pd

from src.pipeline.orchestrator import run_pipeline


def test_run_pipeline_creates_processed_outputs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    data_dir = tmp_path / "data"
    raw_dir = data_dir / "raw"
    processed_dir = data_dir / "processed"
    raw_dir.mkdir(parents=True)
    processed_dir.mkdir(parents=True)

    adspend_df = pd.DataFrame(
        {
            "Campaign_id": ["C1"],
            "Spend": [100],
            "Clicks": [10],
            "Impressions": [1000],
            "Date": ["2025-01-01"],
        }
    )
    interaction_df = pd.DataFrame(
        {
            "User_id": [1],
            "Channel": ["Email"],
            "Interaction_date": ["2025-01-01"],
            "Campaign_id": ["C1"],
        }
    )
    revenue_df = pd.DataFrame(
        {
            "Conversion_id": ["CV1"],
            "User_id": [1],
            "Revenue": [100],
            "Conversion_date": ["2025-01-05"],
        }
    )

    adspend_df.to_csv(raw_dir / "Add Spend Dataset.csv", index=False)
    interaction_df.to_csv(raw_dir / "Customer Interaction Dataset.csv", index=False)
    revenue_df.to_csv(raw_dir / "Revenue Dataset.csv", index=False)

    run_pipeline()

    assert (processed_dir / "adspend_featured.csv").exists()
    assert (processed_dir / "interaction_featured.csv").exists()
    assert (processed_dir / "revenue_featured.csv").exists()
