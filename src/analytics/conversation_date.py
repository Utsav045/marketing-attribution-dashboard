"""
Marketing Attribution Dashboard
Conversion Date Analytics Module

Developer: Isaac

Note:
    The file name in the repository is conversation_date.py.
    The module focuses on conversion date analysis.

Purpose:
    Analyze conversion dates, prepare time based fields and support
    monthly, weekly and daily trend analysis.
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


def convert_to_datetime(
    df: pd.DataFrame,
    date_column: str,
) -> pd.DataFrame:
    """
    Convert a date column to pandas datetime format.
    """

    if date_column not in df.columns:
        raise ValueError(f"Dataframe must contain '{date_column}' column.")

    result = df.copy()
    result[date_column] = pd.to_datetime(result[date_column], errors="coerce")

    return result


def add_date_parts(
    df: pd.DataFrame,
    date_column: str,
) -> pd.DataFrame:
    """
    Add year, quarter, month, week and day fields from a date column.
    """

    if date_column not in df.columns:
        raise ValueError(f"Dataframe must contain '{date_column}' column.")

    result = df.copy()
    result[date_column] = pd.to_datetime(result[date_column], errors="coerce")

    result["year"] = result[date_column].dt.year
    result["quarter"] = result[date_column].dt.quarter
    result["month"] = result[date_column].dt.month
    result["month_name"] = result[date_column].dt.month_name()
    result["week"] = result[date_column].dt.isocalendar().week.astype("Int64")
    result["day"] = result[date_column].dt.day
    result["day_name"] = result[date_column].dt.day_name()
    result["date"] = result[date_column].dt.date

    return result


def add_conversion_periods(
    conversions_df: pd.DataFrame,
    conversion_date_col: str = "conversion_date",
) -> pd.DataFrame:
    """
    Add conversion period fields to conversion data.
    """

    result = add_date_parts(conversions_df, conversion_date_col)

    result["conversion_month"] = result[conversion_date_col].dt.to_period("M").astype(str)
    result["conversion_week"] = result[conversion_date_col].dt.to_period("W").astype(str)
    result["conversion_day"] = result[conversion_date_col].dt.to_period("D").astype(str)

    return result


def summarize_conversions_by_month(
    conversions_df: pd.DataFrame,
    conversion_date_col: str = "conversion_date",
    revenue_col: str = "revenue",
) -> pd.DataFrame:
    """
    Summarize conversions and revenue by month.
    """

    required_columns = {conversion_date_col, revenue_col}
    missing_columns = required_columns.difference(conversions_df.columns)

    if missing_columns:
        raise ValueError(f"Conversion data missing columns: {sorted(missing_columns)}")

    df = conversions_df.copy()
    df[conversion_date_col] = pd.to_datetime(df[conversion_date_col], errors="coerce")
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0)

    df = df.dropna(subset=[conversion_date_col])
    df["conversion_month"] = df[conversion_date_col].dt.to_period("M").astype(str)

    result = (
        df.groupby("conversion_month", as_index=False)
        .agg(
            total_conversions=(conversion_date_col, "count"),
            total_revenue=(revenue_col, "sum"),
            average_revenue=(revenue_col, "mean"),
        )
        .sort_values("conversion_month")
    )

    return result


def summarize_conversions_by_week(
    conversions_df: pd.DataFrame,
    conversion_date_col: str = "conversion_date",
    revenue_col: str = "revenue",
) -> pd.DataFrame:
    """
    Summarize conversions and revenue by week.
    """

    required_columns = {conversion_date_col, revenue_col}
    missing_columns = required_columns.difference(conversions_df.columns)

    if missing_columns:
        raise ValueError(f"Conversion data missing columns: {sorted(missing_columns)}")

    df = conversions_df.copy()
    df[conversion_date_col] = pd.to_datetime(df[conversion_date_col], errors="coerce")
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0)

    df = df.dropna(subset=[conversion_date_col])
    df["conversion_week"] = df[conversion_date_col].dt.to_period("W").astype(str)

    result = (
        df.groupby("conversion_week", as_index=False)
        .agg(
            total_conversions=(conversion_date_col, "count"),
            total_revenue=(revenue_col, "sum"),
            average_revenue=(revenue_col, "mean"),
        )
        .sort_values("conversion_week")
    )

    return result


def summarize_conversions_by_day(
    conversions_df: pd.DataFrame,
    conversion_date_col: str = "conversion_date",
    revenue_col: str = "revenue",
) -> pd.DataFrame:
    """
    Summarize conversions and revenue by day.
    """

    required_columns = {conversion_date_col, revenue_col}
    missing_columns = required_columns.difference(conversions_df.columns)

    if missing_columns:
        raise ValueError(f"Conversion data missing columns: {sorted(missing_columns)}")

    df = conversions_df.copy()
    df[conversion_date_col] = pd.to_datetime(df[conversion_date_col], errors="coerce")
    df[revenue_col] = pd.to_numeric(df[revenue_col], errors="coerce").fillna(0)

    df = df.dropna(subset=[conversion_date_col])
    df["conversion_day"] = df[conversion_date_col].dt.date

    result = (
        df.groupby("conversion_day", as_index=False)
        .agg(
            total_conversions=(conversion_date_col, "count"),
            total_revenue=(revenue_col, "sum"),
            average_revenue=(revenue_col, "mean"),
        )
        .sort_values("conversion_day")
    )

    return result


def get_conversion_date_range(
    conversions_df: pd.DataFrame,
    conversion_date_col: str = "conversion_date",
) -> Dict[str, object]:
    """
    Return the earliest date, latest date and number of active days.
    """

    if conversion_date_col not in conversions_df.columns:
        raise ValueError(
            f"Conversion data must contain '{conversion_date_col}' column."
        )

    df = conversions_df.copy()
    df[conversion_date_col] = pd.to_datetime(df[conversion_date_col], errors="coerce")
    df = df.dropna(subset=[conversion_date_col])

    if df.empty:
        return {
            "start_date": None,
            "end_date": None,
            "active_days": 0,
        }

    start_date = df[conversion_date_col].min()
    end_date = df[conversion_date_col].max()

    active_days = (end_date - start_date).days + 1

    return {
        "start_date": str(start_date.date()),
        "end_date": str(end_date.date()),
        "active_days": int(active_days),
    }


def compare_conversion_periods(
    conversions_df: pd.DataFrame,
    conversion_date_col: str = "conversion_date",
    revenue_col: str = "revenue",
) -> Dict[str, pd.DataFrame]:
    """
    Return daily, weekly and monthly conversion summaries.
    """

    return {
        "daily": summarize_conversions_by_day(
            conversions_df,
            conversion_date_col,
            revenue_col,
        ),
        "weekly": summarize_conversions_by_week(
            conversions_df,
            conversion_date_col,
            revenue_col,
        ),
        "monthly": summarize_conversions_by_month(
            conversions_df,
            conversion_date_col,
            revenue_col,
        ),
    }


if __name__ == "__main__":
    sample_conversions = pd.DataFrame(
        {
            "conversion_id": ["CV001", "CV002", "CV003"],
            "user_id": ["U001", "U002", "U003"],
            "revenue": [2500, 900, 1200],
            "conversion_date": [
                "2026-06-01",
                "2026-06-07",
                "2026-07-02",
            ],
        }
    )

    print(get_conversion_date_range(sample_conversions))
    print(summarize_conversions_by_month(sample_conversions))
    print(summarize_conversions_by_week(sample_conversions))