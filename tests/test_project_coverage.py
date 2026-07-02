import pandas as pd

from src.analytics import eda
from src.analytics import kpi_calculator
from src.analytics.cac import calculate_cac
from src.analytics.roas import calculate_roas, save_roas_results
from src.ingestion.load_data import load_data as load_raw_data
from src.preprocessing.data_cleaner import clean_data
from src.preprocessing.handle_missing import handle_missing
from src.preprocessing.transform_dates import convert_date, transform_dates
from src.utils.constants import CHANNELS, KPIS, ATTRIBUTION_MODELS
from src.utils.file_manager import (
    create_directory,
    delete_file,
    file_exists,
    get_file_size,
    list_files,
    read_csv,
    write_csv,
)
from src.utils.helpers import (
    check_duplicates,
    check_missing_values,
    generate_summary,
    load_csv,
    save_csv,
)


def test_constants_have_expected_values():
    assert "Google Ads" in CHANNELS
    assert "ROI" in KPIS
    assert "First Touch" in ATTRIBUTION_MODELS


def test_helpers_io_and_metrics(tmp_path):
    df = pd.DataFrame({"A": [1, None, 2], "B": [1, 2, 3]})
    path = tmp_path / "sample.csv"

    save_csv(df, path)
    loaded = load_csv(path)

    assert loaded is not None
    assert loaded.shape == (3, 2)
    assert check_duplicates(pd.DataFrame({"X": [1, 1]})) == 1
    assert check_missing_values(df)["A"] == 1
    summary = generate_summary(pd.DataFrame({"X": [1, 2, 3]}))
    assert summary.loc["mean", "X"] == 2.0


def test_file_manager_roundtrip_and_filesystem(tmp_path):
    target_dir = tmp_path / "nested"
    create_directory(target_dir)
    assert target_dir.exists()
    assert file_exists(target_dir)

    csv_file = target_dir / "data.csv"
    write_csv(pd.DataFrame({"A": [1]}), csv_file)
    assert read_csv(csv_file).iloc[0, 0] == 1
    assert "data.csv" in list_files(target_dir)
    assert get_file_size(csv_file) > 0

    delete_file(csv_file)
    assert not csv_file.exists()


def test_clean_data_converts_currency():
    df = pd.DataFrame(
        {"Campaign_id": ["A", "A"], "Spend": ["$10", "$10"], "Revenue": ["$5", "$5"]}
    )
    result = clean_data(df)
    assert result.shape[0] == 1
    assert result["Spend"].iloc[0] == 10.0
    assert result["Revenue"].iloc[0] == 5.0


def test_handle_missing_replaces_none():
    df = pd.DataFrame({"A": [1, None], "B": [None, 2]})
    result = handle_missing(df)
    assert result.loc[0, "B"] == "Unknown"
    assert result.loc[1, "A"] == "Unknown"


def test_transform_date_helpers():
    series = pd.Series(["2025-01-01"])
    converted = convert_date(series)
    assert converted.iloc[0] == "01/01/2025"

    df = pd.DataFrame({"Date": ["2025-01-01"], "Conversion_date": ["2025-01-02"]})
    transformed = transform_dates(df)
    assert transformed.loc[0, "Date"] == "01/01/2025"
    assert transformed.loc[0, "Conversion_date"] == "02/01/2025"


def test_ingestion_data_loader_reads_raw_files(tmp_path, monkeypatch):
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


def test_eda_run_writes_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {"Channel": ["Email"], "Spend": [100], "Revenue": [200], "User_id": [1]}
    ).to_csv(processed_dir / "adspend_featured.csv", index=False)
    pd.DataFrame({"Campaign_id": ["C1"], "User_id": [1], "Channel": ["Email"]}).to_csv(
        processed_dir / "interaction_featured.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Revenue": [200]}).to_csv(
        processed_dir / "revenue_featured.csv", index=False
    )

    eda.run_eda()
    assert (processed_dir / "eda_adspend.csv").exists()
    assert (processed_dir / "eda_interaction.csv").exists()
    assert (processed_dir / "eda_revenue.csv").exists()


def test_kpi_calculator_returns_any_value(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {"Campaign_id": ["C1"], "Spend": [100.0], "Clicks": [10], "Impressions": [1000]}
    ).to_csv(processed_dir / "adspend_featured.csv", index=False)
    pd.DataFrame({"Revenue": [500.0]}).to_csv(
        processed_dir / "revenue_featured.csv", index=False
    )

    kpis = kpi_calculator.calculate_kpis()
    assert kpis["Total Spend"] == 100.0
    assert kpis["ROAS"] == 5.0


def test_cac_calculates_value(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"Spend": [100.0]}).to_csv(
        processed_dir / "adspend_featured.csv", index=False
    )
    pd.DataFrame({"User_id": [1]}).to_csv(
        processed_dir / "interaction_featured.csv", index=False
    )

    calculate_cac()
    captured = capsys.readouterr()
    assert "Total Spend:" in captured.out


def test_calculate_roas_and_save_results(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            "Campaign_id": ["C1"],
            "Channel": ["Email"],
            "Spend": [100.0],
            "Impressions": [1000],
            "Clicks": [10],
        }
    ).to_csv(processed_dir / "adspend_featured_eng.csv", index=False)
    pd.DataFrame({"Campaign_id": ["C1"], "User_id": [1]}).to_csv(
        processed_dir / "interaction_featured_eng.csv", index=False
    )
    pd.DataFrame({"User_id": [1], "Revenue": [500.0]}).to_csv(
        processed_dir / "revenue_featured_eng.csv", index=False
    )

    result = calculate_roas()
    assert result["ROAS"].iloc[0] == 5.0

    save_roas_results(result)
    assert (processed_dir / "roas_results.csv").exists()
