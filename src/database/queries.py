"""
Reusable SQL Query Functions
Multi-Touch Marketing Attribution & ROI Dashboard
"""

import pandas as pd
from sqlalchemy import text
from .db_connection import get_engine


def _query(sql: str) -> pd.DataFrame:
    """Internal helper: run a SELECT query and return a DataFrame."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        columns = list(result.keys())
    return pd.DataFrame(rows, columns=columns)


# ---------------------------------------------------------------------------
# Ad Spend Queries
# ---------------------------------------------------------------------------

def get_spend_by_channel() -> pd.DataFrame:
    """Return total spend grouped by channel."""
    return _query("""
        SELECT channel,
               SUM(spend) AS total_spend,
               SUM(clicks) AS total_clicks,
               SUM(impressions) AS total_impressions
        FROM ad_spend_performance
        GROUP BY channel
        ORDER BY total_spend DESC;
    """)


def get_spend_by_campaign() -> pd.DataFrame:
    """Return total spend grouped by campaign."""
    return _query("""
        SELECT campaign_id,
               SUM(spend) AS total_spend,
               SUM(clicks) AS total_clicks
        FROM ad_spend_performance
        GROUP BY campaign_id
        ORDER BY total_spend DESC;
    """)


# ---------------------------------------------------------------------------
# Revenue Queries
# ---------------------------------------------------------------------------

def get_total_revenue() -> pd.DataFrame:
    """Return total revenue across all conversions."""
    return _query("""
        SELECT
            COUNT(*) AS total_conversions,
            SUM(revenue) AS total_revenue,
            AVG(revenue) AS avg_revenue
        FROM revenue_conversions;
    """)


def get_revenue_by_user() -> pd.DataFrame:
    """Return total revenue per user."""
    return _query("""
        SELECT user_id,
               SUM(revenue) AS total_revenue,
               COUNT(*) AS conversion_count
        FROM revenue_conversions
        GROUP BY user_id
        ORDER BY total_revenue DESC;
    """)


# ---------------------------------------------------------------------------
# KPI Queries
# ---------------------------------------------------------------------------

def get_roi_by_channel() -> pd.DataFrame:
    """
    Calculate ROI per channel by joining spend and revenue tables
    via customer_journeys.
    """
    return _query("""
        SELECT
            asp.channel,
            SUM(asp.spend) AS total_spend,
            SUM(rc.revenue) AS total_revenue,
            CASE
                WHEN SUM(asp.spend) > 0
                THEN ROUND(
                    ((SUM(rc.revenue) - SUM(asp.spend)) / SUM(asp.spend)) * 100, 2
                )
                ELSE 0
            END AS roi_pct
        FROM customer_journeys cj
        JOIN ad_spend_performance asp ON cj.cookie = CAST(asp.campaign_id AS VARCHAR)
        JOIN revenue_conversions rc ON cj.cookie = rc.user_id
        GROUP BY asp.channel
        ORDER BY roi_pct DESC;
    """)


def get_cac_by_channel() -> pd.DataFrame:
    """
    Calculate Customer Acquisition Cost (CAC) per channel.
    CAC = Total Spend / Number of Conversions
    """
    return _query("""
        SELECT
            asp.channel,
            SUM(asp.spend) AS total_spend,
            COUNT(rc.conversion_id) AS total_conversions,
            CASE
                WHEN COUNT(rc.conversion_id) > 0
                THEN ROUND(SUM(asp.spend) / COUNT(rc.conversion_id), 2)
                ELSE 0
            END AS cac
        FROM ad_spend_performance asp
        LEFT JOIN revenue_conversions rc ON rc.user_id IS NOT NULL
        GROUP BY asp.channel
        ORDER BY cac ASC;
    """)


# ---------------------------------------------------------------------------
# Attribution Queries
# ---------------------------------------------------------------------------

def get_customer_journey_summary() -> pd.DataFrame:
    """Return summary of customer journeys with conversion rates."""
    return _query("""
        SELECT
            interaction AS channel,
            COUNT(*) AS total_touchpoints,
            SUM(conversion) AS total_conversions,
            ROUND(AVG(conversion) * 100, 2) AS conversion_rate_pct,
            SUM(revenue) AS total_revenue
        FROM customer_journeys
        GROUP BY interaction
        ORDER BY total_conversions DESC;
    """)


if __name__ == "__main__":
    print("Spend by Channel:")
    print(get_spend_by_channel())
    print("\nTotal Revenue:")
    print(get_total_revenue())
