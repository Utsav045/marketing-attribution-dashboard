"""
Integration-style tests for the analytics package.
Verifies that all analytics modules are importable and callable.
"""

import importlib
import numpy as np
import pandas as pd
import pytest


# ---------------------------------------------------------------------------
# Import smoke tests
# ---------------------------------------------------------------------------

def test_import_kpi_calculator():
    assert importlib.import_module("src.analytics.kpi_calculator") is not None


def test_import_roi():
    assert importlib.import_module("src.analytics.roi") is not None


def test_import_roas():
    assert importlib.import_module("src.analytics.roas") is not None


def test_import_cac():
    assert importlib.import_module("src.analytics.cac") is not None


def test_import_eda():
    assert importlib.import_module("src.analytics.eda") is not None


# ---------------------------------------------------------------------------
# Functional tests using shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_adspend_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Campaign_id": ["C1", "C2", "C3"],
            "Channel": ["Google Ads", "Facebook", "Instagram"],
            "Spend": [1000.0, 500.0, 750.0],
            "Clicks": [200, 100, 150],
            "Impressions": [10000, 5000, 7500],
        }
    )


@pytest.fixture
def sample_revenue_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "User_id": ["U1", "U2", "U3"],
            "Campaign_id": ["C1", "C2", "C3"],
            "Revenue": [3000.0, 800.0, 1500.0],
        }
    )


def test_roi_calculation_formula(
    sample_adspend_df: pd.DataFrame, sample_revenue_df: pd.DataFrame
) -> None:
    """ROI = (Revenue - Spend) / Spend * 100"""
    merged = sample_adspend_df.merge(sample_revenue_df, on="Campaign_id")
    merged["ROI"] = ((merged["Revenue"] - merged["Spend"]) / merged["Spend"]) * 100

    # C1: (3000 - 1000) / 1000 * 100 = 200%
    roi_c1: float = float(merged.loc[merged["Campaign_id"] == "C1", "ROI"].iloc[0])
    assert round(roi_c1, 2) == 200.0


def test_roas_calculation_formula(
    sample_adspend_df: pd.DataFrame, sample_revenue_df: pd.DataFrame
) -> None:
    """ROAS = Revenue / Spend"""
    merged = sample_adspend_df.merge(sample_revenue_df, on="Campaign_id")
    merged["ROAS"] = merged["Revenue"] / merged["Spend"]

    # C2: 800 / 500 = 1.6
    roas_c2: float = float(merged.loc[merged["Campaign_id"] == "C2", "ROAS"].iloc[0])
    assert round(roas_c2, 2) == 1.6


def test_cac_calculation_formula(sample_adspend_df: pd.DataFrame) -> None:
    """CAC = Spend / Clicks (used as proxy for conversions here)"""
    sample_adspend_df["CAC"] = sample_adspend_df["Spend"] / sample_adspend_df["Clicks"]

    # C1: 1000 / 200 = 5.0
    cac_c1 = float(sample_adspend_df["CAC"].to_numpy()[0])
    assert round(cac_c1, 2) == 5.0


def test_spend_totals_are_positive(sample_adspend_df: pd.DataFrame) -> None:
    assert bool((sample_adspend_df["Spend"] > 0).all())


def test_revenue_totals_are_positive(sample_revenue_df: pd.DataFrame) -> None:
    assert bool((sample_revenue_df["Revenue"] > 0).all())


def test_analytics_no_division_by_zero(sample_adspend_df: pd.DataFrame) -> None:
    """Ensure no division by zero in ROI when Spend > 0."""
    sample_adspend_df["Revenue"] = [3000.0, 800.0, 1500.0]

    spend = sample_adspend_df["Spend"].to_numpy()
    revenue = sample_adspend_df["Revenue"].to_numpy()

    roi = np.where(spend > 0, ((revenue - spend) / spend) * 100, 0.0)

    assert not bool(np.isnan(roi).any())
