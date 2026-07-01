"""
Marketing Attribution Dashboard
Return on Ad Spend Module

Developer: Isaac

Purpose:
    Calculate ROAS at executive, channel, campaign and attribution
    model levels.
"""

from __future__ import annotations

import pandas as pd


def _safe_divide(numerator: float, denominator: float) -> float:
    """Return safe division result."""

    if denominator is None or denominator == 0:
        return 0.0

    return float(numerator) / float(denominator)


def _clean_numeric(series: pd.Series) -> pd.Series:
    """Convert a pandas Series to numeric values."""

    return (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"": "0", "nan": "0", "None": "0"})
        .pipe(pd.to_numeric, errors="coerce")
        .fillna(0)
    )


def calculate_total_roas(
    ad_spend_df: pd.DataFrame,
    conversions_df: pd.DataFrame,
) -> float:
    """
    Calculate overall ROAS.

    Formula:
        ROAS = Total Revenue / Total Spend
    """

    if "spend" not in ad_spend_df.columns:
        raise ValueError("ad_spend_df must contain a 'spend' column.")

    if "revenue" not in conversions_df.columns:
        raise ValueError("conversions_df must contain a 'revenue' column.")

    total_spend = _clean_numeric(ad_spend_df["spend"]).sum()
    total_revenue = _clean_numeric(conversions_df["revenue"]).sum()

    return round(_safe_divide(total_revenue, total_spend), 4)


def calculate_channel_roas(
    ad_spend_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    channel_col: str = "channel",
) -> pd.DataFrame:
    """
    Calculate ROAS by channel.

    Formula:
        Channel ROAS = Channel Attributed Revenue / Channel Spend
    """

    required_spend_columns = {channel_col, "spend"}
    required_attr_columns = {channel_col, "attributed_revenue"}

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
    attr_df["attributed_revenue"] = _clean_numeric(attr_df["attributed_revenue"])

    spend_summary = (
        spend_df.groupby(channel_col, as_index=False)
        .agg(total_spend=("spend", "sum"))
    )

    revenue_summary = (
        attr_df.groupby(channel_col, as_index=False)
        .agg(attributed_revenue=("attributed_revenue", "sum"))
    )

    result = spend_summary.merge(revenue_summary, on=channel_col, how="left")

    result["attributed_revenue"] = result["attributed_revenue"].fillna(0)

    result["roas"] = result.apply(
        lambda row: _safe_divide(row["attributed_revenue"], row["total_spend"]),
        axis=1,
    )

    return result.sort_values("roas", ascending=False)


def calculate_campaign_roas(
    ad_spend_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    campaign_col: str = "campaign_id",
) -> pd.DataFrame:
    """
    Calculate ROAS by campaign.

    Formula:
        Campaign ROAS = Campaign Attributed Revenue / Campaign Spend
    """

    required_spend_columns = {campaign_col, "spend"}
    required_attr_columns = {campaign_col, "attributed_revenue"}

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
    attr_df["attributed_revenue"] = _clean_numeric(attr_df["attributed_revenue"])

    spend_summary = (
        spend_df.groupby(campaign_col, as_index=False)
        .agg(total_spend=("spend", "sum"))
    )

    revenue_summary = (
        attr_df.groupby(campaign_col, as_index=False)
        .agg(attributed_revenue=("attributed_revenue", "sum"))
    )

    result = spend_summary.merge(revenue_summary, on=campaign_col, how="left")

    result["attributed_revenue"] = result["attributed_revenue"].fillna(0)

    result["roas"] = result.apply(
        lambda row: _safe_divide(row["attributed_revenue"], row["total_spend"]),
        axis=1,
    )

    return result.sort_values("roas", ascending=False)


def calculate_roas_by_model(
    ad_spend_df: pd.DataFrame,
    attribution_df: pd.DataFrame,
    model_col: str = "attribution_model",
) -> pd.DataFrame:
    """
    Calculate ROAS by attribution model.

    This helps compare how total return changes under different
    attribution models.
    """

    if "spend" not in ad_spend_df.columns:
        raise ValueError("ad_spend_df must contain a 'spend' column.")

    required_attr_columns = {model_col, "attributed_revenue"}

    missing_attr = required_attr_columns.difference(attribution_df.columns)

    if missing_attr:
        raise ValueError(f"attribution_df missing columns: {sorted(missing_attr)}")

    total_spend = _clean_numeric(ad_spend_df["spend"]).sum()

    attr_df = attribution_df.copy()
    attr_df["attributed_revenue"] = _clean_numeric(attr_df["attributed_revenue"])

    model_summary = (
        attr_df.groupby(model_col, as_index=False)
        .agg(attributed_revenue=("attributed_revenue", "sum"))
    )

    model_summary["total_spend"] = total_spend

    model_summary["roas"] = model_summary.apply(
        lambda row: _safe_divide(row["attributed_revenue"], row["total_spend"]),
        axis=1,
    )

    return model_summary.sort_values("roas", ascending=False)


def classify_roas(roas_value: float) -> str:
    """
    Classify ROAS result for reporting.
    """

    if roas_value >= 4:
        return "excellent"

    if roas_value >= 2:
        return "good"

    if roas_value >= 1:
        return "break-even or low return"

    return "poor"


def explain_roas() -> str:
    """Return a plain explanation of ROAS."""

    return (
        "Return on Ad Spend measures how much revenue is generated for every "
        "unit spent on advertising. A ROAS of 4 means that the business "
        "generated 4 units of revenue for every 1 unit spent."
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
            "revenue": [2500, 1800, 600],
        }
    )

    sample_attribution = pd.DataFrame(
        {
            "campaign_id": ["C001", "C002", "C003"],
            "channel": ["Google", "Facebook", "Email"],
            "attributed_revenue": [2500, 1800, 600],
            "attribution_model": ["LINEAR", "LINEAR", "LINEAR"],
        }
    )

    total_roas = calculate_total_roas(sample_spend, sample_conversions)

    print("Overall ROAS:", total_roas)
    print("ROAS Classification:", classify_roas(total_roas))
    print(calculate_channel_roas(sample_spend, sample_attribution))