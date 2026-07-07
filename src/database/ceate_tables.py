"""
Create Database Tables Module
Multi-Touch Marketing Attribution & ROI Dashboard
"""

from .db_connection import get_connection


CREATE_CUSTOMER_JOURNEYS = """
CREATE TABLE IF NOT EXISTS customer_journeys (
    journey_id SERIAL PRIMARY KEY,
    cookie VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    interaction VARCHAR(100),
    conversion SMALLINT DEFAULT 0,
    revenue DECIMAL(12, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CAMPAIGNS = """
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id VARCHAR(50) PRIMARY KEY,
    campaign_name VARCHAR(200),
    channels_used VARCHAR(200),
    duration_days INTEGER,
    clicks BIGINT DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    acquisition_cost DECIMAL(14, 2),
    roi_pct DECIMAL(8, 2),
    location VARCHAR(100),
    language VARCHAR(50)
);
"""

CREATE_AD_SPEND_PERFORMANCE = """
CREATE TABLE IF NOT EXISTS ad_spend_performance (
    spend_id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(50),
    channel VARCHAR(100) NOT NULL,
    spend DECIMAL(14, 2) DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    spend_date DATE NOT NULL,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id) ON DELETE SET NULL
);
"""

CREATE_REVENUE_CONVERSIONS = """
CREATE TABLE IF NOT EXISTS revenue_conversions (
    conversion_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    revenue DECIMAL(12, 2) DEFAULT 0,
    conversion_date VARCHAR(50)
);
"""

CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_journeys_cookie ON customer_journeys(cookie);
CREATE INDEX IF NOT EXISTS idx_spend_campaign ON ad_spend_performance(campaign_id);
CREATE INDEX IF NOT EXISTS idx_revenue_user ON revenue_conversions(user_id);
"""


def create_all_tables() -> None:
    """
    Create all required tables in the PostgreSQL database.
    Uses IF NOT EXISTS to avoid errors on re-runs.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        print("[INFO] Creating tables...")

        cursor.execute(CREATE_CUSTOMER_JOURNEYS)
        print("  ✓ customer_journeys")

        cursor.execute(CREATE_CAMPAIGNS)
        print("  ✓ campaigns")

        cursor.execute(CREATE_AD_SPEND_PERFORMANCE)
        print("  ✓ ad_spend_performance")

        cursor.execute(CREATE_REVENUE_CONVERSIONS)
        print("  ✓ revenue_conversions")

        cursor.execute(CREATE_INDEXES)
        print("  ✓ Indexes created")

        conn.commit()
        print("[INFO] All tables created successfully.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Table creation failed: {e}")
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_all_tables()
