import pandas as pd

from src.preprocessing.transform_dates import convert_date, transform_dates


def test_convert_date_formats_date_series():
    series = pd.Series(["2025-01-01", "2025-02-03"])

    result = convert_date(series)

    assert result.iloc[0] == "01/01/2025"
    assert result.iloc[1] == "03/02/2025"


def test_transform_dates_formats_date_columns():
    df = pd.DataFrame({"Date": ["2025-01-02"], "Conversion_date": ["2025-02-03"]})

    result = transform_dates(df)

    assert result.loc[0, "Date"].endswith("2025")
    assert result.loc[0, "Conversion_date"].endswith("2025")


def test_run_transform_dates_writes_files(tmp_path, monkeypatch):
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)
    pd.DataFrame({"Date": ["2025-01-02"]}).to_csv(
        processed_dir / "cleaned_add_spend_dataset.csv", index=False
    )
    pd.DataFrame({"Conversion_date": ["2025-02-03"]}).to_csv(
        processed_dir / "cleaned_customer_interaction_dataset.csv", index=False
    )
    pd.DataFrame({"Date": ["2025-01-03"]}).to_csv(
        processed_dir / "cleaned_revenue_dataset.csv", index=False
    )

    monkeypatch.chdir(tmp_path)
    from src.preprocessing.transform_dates import run_transform_dates

    run_transform_dates()

    assert (processed_dir / "cleaned_add_spend_dataset.csv").exists()
    assert (processed_dir / "cleaned_customer_interaction_dataset.csv").exists()
    assert (processed_dir / "cleaned_revenue_dataset.csv").exists()
