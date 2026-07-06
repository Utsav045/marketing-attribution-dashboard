"""
Load Processed Data into PostgreSQL
Multi-Touch Marketing Attribution & ROI Dashboard
"""

import pandas as pd
from pathlib import Path
from .db_connection import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_ad_spend(conn) -> None:
    """Load adspend_featured.csv into ad_spend_performance table."""
    filepath = PROCESSED_DIR / "adspend_featured.csv"
    if not filepath.exists():
        print(f"[WARN] File not found: {filepath}")
        return

    df = pd.read_csv(filepath)
    cursor = conn.cursor()

    rows_inserted = 0
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO ad_spend_performance (campaign_id, channel, spend, clicks, impressions, spend_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (
                row.get("Campaign_id"),
                row.get("Channel"),
                row.get("Spend", 0),
                row.get("Clicks", 0),
                row.get("Impressions", 0),
                row.get("Date"),
            ),
        )
        rows_inserted += 1

    conn.commit()
    cursor.close()
    print(f"[INFO] ad_spend_performance: {rows_inserted} rows inserted.")


def load_revenue(conn) -> None:
    """Load revenue_featured.csv into revenue_conversions table."""
    filepath = PROCESSED_DIR / "revenue_featured.csv"
    if not filepath.exists():
        print(f"[WARN] File not found: {filepath}")
        return

    df = pd.read_csv(filepath)
    cursor = conn.cursor()

    rows_inserted = 0
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO revenue_conversions (conversion_id, user_id, revenue, conversion_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (conversion_id) DO NOTHING;
            """,
            (
                row.get("Conversion_id", str(rows_inserted)),
                row.get("User_id"),
                row.get("Revenue", 0),
                row.get("Conversion_Date"),
            ),
        )
        rows_inserted += 1

    conn.commit()
    cursor.close()
    print(f"[INFO] revenue_conversions: {rows_inserted} rows inserted.")


def load_interactions(conn) -> None:
    """Load interaction_featured.csv into customer_journeys table."""
    filepath = PROCESSED_DIR / "interaction_featured.csv"
    if not filepath.exists():
        print(f"[WARN] File not found: {filepath}")
        return

    df = pd.read_csv(filepath)
    cursor = conn.cursor()

    rows_inserted = 0
    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO customer_journeys (cookie, timestamp, interaction, conversion, revenue)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                row.get("User_id"),
                row.get("Timestamp", row.get("Date")),
                row.get("Channel"),
                int(row.get("Conversion", 0)),
                row.get("Revenue", 0),
            ),
        )
        rows_inserted += 1

    conn.commit()
    cursor.close()
    print(f"[INFO] customer_journeys: {rows_inserted} rows inserted.")


def load_all_data() -> None:
    """
    Load all processed CSV datasets into PostgreSQL tables.
    """
    print("=" * 50)
    print("LOADING DATA TO POSTGRESQL")
    print("=" * 50)

    conn = get_connection()

    try:
        load_ad_spend(conn)
        load_revenue(conn)
        load_interactions(conn)
        print("\n[INFO] All data loaded successfully.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Data loading failed: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    load_all_data()
