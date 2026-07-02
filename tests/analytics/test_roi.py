import pandas as pd

from src.analytics.roi import calculate_roi


def test_calculate_roi_with_sample_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame(
        {"Campaign_id": ["C1"], "Channel": ["Email"], "Spend": [100.0]}
    ).to_csv(processed_dir / "adspend_featured_eng.csv", index=False)

    pd.DataFrame({"User_id": [1], "Campaign_id": ["C1"]}).to_csv(
        processed_dir / "interaction_featured_eng.csv", index=False
    )

    pd.DataFrame({"User_id": [1], "Revenue": [500.0]}).to_csv(
        processed_dir / "revenue_featured_eng.csv", index=False
    )

    result = calculate_roi()

    assert "ROI" in result.columns
    assert result["ROI"].iloc[0] == 400.0


def test_calculate_roi_handles_zero_spend(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame({"Campaign_id": ["C1"], "Channel": ["Email"], "Spend": [0.0]}).to_csv(
        processed_dir / "adspend_featured_eng.csv", index=False
    )

    pd.DataFrame({"User_id": [1], "Campaign_id": ["C1"]}).to_csv(
        processed_dir / "interaction_featured_eng.csv", index=False
    )

    pd.DataFrame({"User_id": [1], "Revenue": [500.0]}).to_csv(
        processed_dir / "revenue_featured_eng.csv", index=False
    )

    result = calculate_roi()

    assert result["ROI"].iloc[0] == 0
