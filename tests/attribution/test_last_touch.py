import pandas as pd

from src.attribution.last_touch import last_touch_attribution


def test_last_touch_attribution_writes_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    journey_df = pd.DataFrame(
        {
            "User_id": [1, 2],
            "Journey": ["Email > Social", "Social"],
            "Revenue": [100, 200],
        }
    )
    journey_df.to_csv(processed_dir / "customer_journeys.csv", index=False)

    last_touch_attribution()

    result = pd.read_csv(processed_dir / "last_touch_results.csv")
    assert len(result) == 1
    assert result.loc[0, "Last_Touch"] == "Social"
