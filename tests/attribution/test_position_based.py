import pandas as pd

from src.attribution.position_based import position_based_attribution


def test_position_based_attribution_writes_output(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    journey_df = pd.DataFrame(
        {
            "User_id": [1],
            "Journey": ["Email > Social"],
            "Revenue": [100],
        }
    )
    journey_df.to_csv(processed_dir / "customer_journeys.csv", index=False)

    position_based_attribution()

    output_path = processed_dir / "position_based_attribution.csv"
    assert output_path.exists()
    result = pd.read_csv(output_path)
    assert {"Channel", "Attributed_Revenue"}.issubset(result.columns)
