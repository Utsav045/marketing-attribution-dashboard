import pandas as pd

from src.attribution.attribution_engine import build_customer_journeys


def test_build_customer_journeys_creates_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    interaction_df = pd.DataFrame(
        {
            "User_id": [1, 1, 2],
            "Interaction_date": ["2025-01-01", "2025-01-02", "2025-01-03"],
            "Channel": ["Email", "Social", "Email"],
            "Campaign_id": ["C1", "C2", "C3"],
        }
    )
    revenue_df = pd.DataFrame(
        {
            "Conversion_id": ["CV1", "CV2"],
            "User_id": [1, 2],
            "Revenue": [100, 200],
            "Conversion_date": ["2025-01-05", "2025-01-06"],
        }
    )

    interaction_df.to_csv(processed_dir / "cleaned_customer_interaction_dataset.csv", index=False)
    revenue_df.to_csv(processed_dir / "cleaned_revenue_dataset.csv", index=False)

    build_customer_journeys()

    output_path = processed_dir / "customer_journeys.csv"
    result = pd.read_csv(output_path)

    assert output_path.exists()
    assert {"User_id", "Journey", "Journey_Length"}.issubset(result.columns)
