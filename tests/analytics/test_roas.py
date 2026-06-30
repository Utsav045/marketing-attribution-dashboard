import pandas as pd

from src.analytics.roas import calculate_roas, save_roas_results


def test_calculate_roas_with_sample_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame(
        {"Campaign_id": ["C1"], "Channel": ["Email"], "Spend": [100.0]}
    ).to_csv(processed_dir / "adspend_featured_eng.csv", index=False)

    pd.DataFrame(
        {"User_id": [1], "Campaign_id": ["C1"]}
    ).to_csv(processed_dir / "interaction_featured_eng.csv", index=False)

    pd.DataFrame(
        {"User_id": [1], "Revenue": [500.0]}
    ).to_csv(processed_dir / "revenue_featured_eng.csv", index=False)

    result = calculate_roas()

    assert "ROAS" in result.columns
    assert result["ROAS"].iloc[0] == 5.0


def test_calculate_roas_handles_zero_spend(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame(
        {"Campaign_id": ["C1"], "Channel": ["Email"], "Spend": [0.0]}
    ).to_csv(processed_dir / "adspend_featured_eng.csv", index=False)

    pd.DataFrame(
        {"User_id": [1], "Campaign_id": ["C1"]}
    ).to_csv(processed_dir / "interaction_featured_eng.csv", index=False)

    pd.DataFrame(
        {"User_id": [1], "Revenue": [500.0]}
    ).to_csv(processed_dir / "revenue_featured_eng.csv", index=False)

    result = calculate_roas()

    assert result["ROAS"].iloc[0] == 0


def test_save_roas_results_writes_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    df = pd.DataFrame(
        {
            "User_id": [1],
            "Campaign_id": ["C1"],
            "Channel": ["Email"],
            "Spend": [100.0],
            "Revenue": [500.0],
            "ROAS": [5.0],
        }
    )

    save_roas_results(df)

    output_path = processed_dir / "roas_results.csv"
    assert output_path.exists()
    saved = pd.read_csv(output_path)
    assert saved["ROAS"].iloc[0] == 5.0
