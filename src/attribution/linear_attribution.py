from __future__ import annotations

import pandas as pd
from typing import Optional


def _parse_revenue_value(raw_revenue: object) -> Optional[float]:

    if raw_revenue is None:
        return None

    raw_str = str(raw_revenue).strip().lower()
    if raw_str in {"", "nan", "null", "na", "<na>"}:
        return None

    try:
        normalized = raw_str.replace("$", "").replace(",", "").strip()
        return float(normalized)
    except (ValueError, TypeError):
        return None


def compute_linear_attribution(df: pd.DataFrame) -> pd.DataFrame:
    attribution_rows = []

    for _, row in df.iterrows():
        channels = str(row["Journey"]).split(" > ")
        revenue_value = _parse_revenue_value(row["Revenue"])

        if revenue_value is None or len(channels) == 0:
            continue

        credit_per_channel = revenue_value / len(channels)

        for channel in channels:
            attribution_rows.append(
                {"Channel": channel, "Attributed_Revenue": credit_per_channel}
            )

    result_df = pd.DataFrame(attribution_rows)
    if result_df.empty:
        return result_df

    result_df = result_df.groupby("Channel")["Attributed_Revenue"].sum().reset_index()

    result_df = result_df.sort_values(by="Attributed_Revenue", ascending=False)

    return result_df


def linear_attribution() -> None:
    df = pd.read_csv("data/processed/customer_journeys.csv")
    result_df = compute_linear_attribution(df)

    result_df.to_csv("data/processed/linear_attribution_results.csv", index=False)

    print("\nLinear Attribution Results")
    print(result_df.head())
    print("\nSaved to: data/processed/linear_attribution_results.csv")


if __name__ == "__main__":
    linear_attribution()
