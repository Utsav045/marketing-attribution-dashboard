"""
Marketing Attribution Dashboard
Customer Acquisition Cost Module

Developer: Isaac

Purpose:
    Calculate Customer Acquisition Cost at executive, channel,
    campaign and attribution model levels.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd


def _safe_divide(numerator: float, denominator: float) -> float:
    """Return safe division result."""

    if denominator is None or denominator == 0:
        return 0.0

    return float(numerator) / float(denominator)


def _clean_numeric(series: pd.Series) -> pd.Series:
    """Convert values to numeric after removing common formatting."""

    return (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"": "0", "nan": "0", "None": "0"})
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0)
    )


def calculate_total_cac(
    ad_spend_df: pd.DataFrame,
    conversions_df: pd.DataFrame,
) -> float:
    """
    Calculate overall Customer Acquisition Cost.

    Formula:
        CAC = Total Spend / Number of Acquired Customers

    Required ad_spend_df columns:
        spend

    Required conversions_df columns:
        user_id
    """

    if "spend" not in ad_spend_df.columns:
        raise ValueError("ad_spend_df must contain a 'spend' column.")

    if "user_id" not in conversions_df.columns:
        raise ValueError("conversions_df must contain a 'user_id' column.")

    spend = _clean_numeric(ad_spend_df["spend"]).sum()
    acquired_customers = conversions_df["user_id"].astype(str).nunique()

    return round(_safe_divide(spend, acquired_customers), 4)


def calculate_channel_cac(
    ad_spend_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    channel_col: str = "channel",
) -> pd.DataFrame:
    """
    Calculate CAC by marketing channel.

    Formula:
        Channel CAC = Channel Spend / Channel Conversion Credit

    Required ad_spend_df columns:
        channel
        spend

    Required attribution_df columns:
        channel
        attribution_weight
    """

    required_spend_columns = {channel_col, "spend"}
    required_attr_columns = {channel_col, "attribution_weight"}

    missing_spend = required_spend_columns.difference(ad_spend_df.columns)
    missing_attr = required_attr_columns.difference(attribution_df.columns)

    if missing_spend:
        raise ValueError(f"ad_spend_df missing columns: {sorted(missing_spend)}")

    if missing_attr:
        raise ValueError(f"attribution_df missing columns: {sorted(missing_attr)}")

    spend_df = ad_spend_df.copy()
    attr_df = attribution_df.copy()

    spend_df[channel_col] = spend_df[channel_col].astype(str).str.strip().str.lower()
    attr_df[channel_col] = attr_df[channel_col].astype(str).str.strip().str.lower()

    spend_df["spend"] = _clean_numeric(spend_df["spend"])
    attr_df["attribution_weight"] = _clean_numeric(attr_df["attribution_weight"])

    spend_summary = (
        spend_df.groupby(channel_col, as_index=False)
        .agg(total_spend=("spend", "sum"))
    )

    credit_summary = (
        attr_df.groupby(channel_col, as_index=False)
        .agg(conversion_credit=("attribution_weight", "sum"))
    )

    result = spend_summary.merge(credit_summary, on=channel_col, how="left")

    result["conversion_credit"] = result["conversion_credit"].fillna(0)

    result["cac"] = result.apply(
        lambda row: _safe_divide(row["total_spend"], row["conversion_credit"]),
        axis=1,
    )

    return result.sort_values("cac", ascending=True)


def calculate_campaign_cac(
    ad_spend_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    campaign_col: str = "campaign_id",
) -> pd.DataFrame:
    """
    Calculate CAC by campaign.

    Formula:
        Campaign CAC = Campaign Spend / Campaign Conversion Credit
    """

    required_spend_columns = {campaign_col, "spend"}
    required_attr_columns = {campaign_col, "attribution_weight"}

    missing_spend = required_spend_columns.difference(ad_spend_df.columns)
    missing_attr = required_attr_columns.difference(attribution_df.columns)

    if missing_spend:
        raise ValueError(f"ad_spend_df missing columns: {sorted(missing_spend)}")

    if missing_attr:
        raise ValueError(f"attribution_df missing columns: {sorted(missing_attr)}")

    spend_df = ad_spend_df.copy()
    attr_df = attribution_df.copy()

    spend_df[campaign_col] = spend_df[campaign_col].astype(str).str.strip()
    attr_df[campaign_col] = attr_df[campaign_col].astype(str).str.strip()

    spend_df["spend"] = _clean_numeric(spend_df["spend"])
    attr_df["attribution_weight"] = _clean_numeric(attr_df["attribution_weight"])

    spend_summary = (
        spend_df.groupby(campaign_col, as_index=False)
        .agg(total_spend=("spend", "sum"))
    )

    credit_summary = (
        attr_df.groupby(campaign_col, as_index=False)
        .agg(conversion_credit=("attribution_weight", "sum"))
    )

    result = spend_summary.merge(credit_summary, on=campaign_col, how="left")

    result["conversion_credit"] = result["conversion_credit"].fillna(0)

    result["cac"] = result.apply(
        lambda row: _safe_divide(row["total_spend"], row["conversion_credit"]),
        axis=1,
    )

    return result.sort_values("cac", ascending=True)


def calculate_cac_by_model(
    ad_spend_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    model_col: str = "attribution_model",
) -> pd.DataFrame:
    """
    Calculate CAC by attribution model.

    This helps compare customer acquisition cost under different
    attribution models such as first touch, last touch, linear,
    time decay and position based attribution.
    """

    if "spend" not in ad_spend_df.columns:
        raise ValueError("ad_spend_df must contain a 'spend' column.")

    required_attr_columns = {model_col, "attribution_weight"}

    missing_attr = required_attr_columns.difference(attribution_df.columns)

    if missing_attr:
        raise ValueError(f"attribution_df missing columns: {sorted(missing_attr)}")

    total_spend = _clean_numeric(ad_spend_df["spend"]).sum()

    attr_df = attribution_df.copy()
    attr_df["attribution_weight"] = _clean_numeric(attr_df["attribution_weight"])

    model_summary = (
        attr_df.groupby(model_col, as_index=False)
        .agg(conversion_credit=("attribution_weight", "sum"))
    )

    model_summary["total_spend"] = total_spend

    model_summary["cac"] = model_summary.apply(
        lambda row: _safe_divide(row["total_spend"], row["conversion_credit"]),
        axis=1,
    )

    return model_summary.sort_values("cac", ascending=True)


def explain_cac() -> str:
    """Return a plain explanation of CAC."""

    return (
        "Customer Acquisition Cost measures how much the business spends "
        "to acquire one converting customer. It is calculated as total "
        "marketing spend divided by the number of acquired customers or "
        "conversion credits."
    )


if __name__ == "__main__":
    sample_spend = pd.DataFrame(
        {
            "campaign_id": ["C001", "C002", "C003"],
            "channel": ["Google", "Facebook", "Email"],
            "spend": [1000, 800, 300],
        }
    )

    sample_conversions = pd.DataFrame(
        {
            "conversion_id": ["CV001", "CV002", "CV003"],
            "user_id": ["U001", "U002", "U003"],
        }
    )

    sample_attribution = pd.DataFrame(
        {
            "campaign_id": ["C001", "C002", "C003"],
            "channel": ["Google", "Facebook", "Email"],
            "attribution_model": ["LINEAR", "LINEAR", "LINEAR"],
            "attribution_weight": [1.5, 1.0, 0.5],
        }
    )

    print("Overall CAC:", calculate_total_cac(sample_spend, sample_conversions))
    print(calculate_channel_cac(sample_spend, sample_attribution))