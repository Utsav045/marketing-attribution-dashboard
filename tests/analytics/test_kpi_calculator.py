import pandas as pd

from src.analytics import kpi_calculator


def test_kpi_calculator_module_loads():
    assert kpi_calculator is not None


def test_calculate_kpis_returns_expected_values(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame(
        {"Campaign_id": ["C1"], "Spend": [100.0], "Clicks": [10], "Impressions": [1000]}
    ).to_csv(processed_dir / "adspend_featured.csv", index=False)
    pd.DataFrame({"Revenue": [500.0]}).to_csv(
        processed_dir / "revenue_featured.csv", index=False
    )

    kpis = kpi_calculator.calculate_kpis()

    assert kpis["Total Spend"] == 100.0
    assert kpis["Total Revenue"] == 500.0
    assert kpis["ROAS"] == 5.0


def test_save_kpis_writes_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    pd.DataFrame(
        {"Campaign_id": ["C1"], "Spend": [100.0], "Clicks": [10], "Impressions": [1000]}
    ).to_csv(processed_dir / "adspend_featured.csv", index=False)
    pd.DataFrame({"Revenue": [500.0]}).to_csv(
        processed_dir / "revenue_featured.csv", index=False
    )

    kpi_calculator.save_kpis()

    assert (processed_dir / "kpi_summary.csv").exists()
