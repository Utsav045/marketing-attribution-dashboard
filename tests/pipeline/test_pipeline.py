"""
Pipeline Integration Tests
Verifies the pipeline modules are importable and the orchestrator
is callable end-to-end using temporary test data.
"""

import importlib
import pandas as pd
import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Import smoke tests
# ---------------------------------------------------------------------------

def test_import_orchestrator():
    assert importlib.import_module("src.pipeline.orchestrator") is not None


def test_import_run_pipeline():
    assert importlib.import_module("src.pipeline.run_pipeline") is not None


# ---------------------------------------------------------------------------
# Orchestrator unit tests (mocked file I/O)
# ---------------------------------------------------------------------------

@pytest.fixture
def tmp_pipeline_dirs(tmp_path: Path):
    """Create minimal raw CSVs that the orchestrator can ingest."""
    raw_dir = tmp_path / "data" / "raw"
    raw_dir.mkdir(parents=True)
    processed_dir = tmp_path / "data" / "processed"
    processed_dir.mkdir(parents=True)

    # Ad Spend
    pd.DataFrame(
        {
            "Campaign_id": ["C1", "C2"],
            "Channel": ["Google Ads", "Facebook"],
            "Spend": ["$1000", "$500"],
            "Clicks": [200, 100],
            "Impressions": [10000, 5000],
            "Date": ["2024-01-01", "2024-01-02"],
        }
    ).to_csv(raw_dir / "Add Spend Dataset.csv", index=False)

    # Customer Interaction
    pd.DataFrame(
        {
            "User_id": ["U1", "U2"],
            "Campaign_id": ["C1", "C2"],
            "Channel": ["Google Ads", "Facebook"],
            "Timestamp": ["2024-01-01", "2024-01-02"],
            "Conversion": [1, 0],
        }
    ).to_csv(raw_dir / "Customer Interaction Dataset.csv", index=False)

    # Revenue
    pd.DataFrame(
        {
            "User_id": ["U1", "U2"],
            "Revenue": ["$3000", "$800"],
            "Conversion_Date": ["2024-01-05", "2024-01-06"],
        }
    ).to_csv(raw_dir / "Revenue Dataset.csv", index=False)

    return tmp_path


def test_run_pipeline_returns_three_dataframes(tmp_pipeline_dirs, monkeypatch):
    """
    Patch read_csv / chdir so orchestrator uses temp data,
    then verify it returns (adspend_df, interaction_df, revenue_df).
    """
    monkeypatch.chdir(tmp_pipeline_dirs)

    from src.pipeline.orchestrator import run_pipeline

    result = run_pipeline()

    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 3

    adspend_df, interaction_df, revenue_df = result
    assert isinstance(adspend_df, pd.DataFrame)
    assert isinstance(interaction_df, pd.DataFrame)
    assert isinstance(revenue_df, pd.DataFrame)


def test_pipeline_outputs_are_not_empty(tmp_pipeline_dirs, monkeypatch):
    """Processed DataFrames must have at least one row."""
    monkeypatch.chdir(tmp_pipeline_dirs)

    from src.pipeline.orchestrator import run_pipeline

    adspend_df, interaction_df, revenue_df = run_pipeline()

    assert len(adspend_df) > 0
    assert len(interaction_df) > 0
    assert len(revenue_df) > 0


def test_pipeline_saves_processed_csvs(tmp_pipeline_dirs, monkeypatch):
    """Orchestrator must write the three processed CSV files."""
    monkeypatch.chdir(tmp_pipeline_dirs)

    from src.pipeline.orchestrator import run_pipeline
    run_pipeline()

    processed_dir = tmp_pipeline_dirs / "data" / "processed"
    assert (processed_dir / "adspend_featured.csv").exists()
    assert (processed_dir / "interaction_featured.csv").exists()
    assert (processed_dir / "revenue_featured.csv").exists()
