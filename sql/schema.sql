-- ============================================================
-- MARKETING ATTRIBUTION DASHBOARD
-- DATABASE SCHEMA DESIGN
-- Developer: Isaac
-- Purpose: Create analytical database structure for attribution
-- ============================================================

CREATE SCHEMA IF NOT EXISTS marketing;

SET search_path TO marketing;

-- ============================================================
-- DROP EXISTING TABLES
-- Use carefully during development
-- ============================================================

DROP TABLE IF EXISTS fact_attribution CASCADE;
DROP TABLE IF EXISTS fact_conversions CASCADE;
DROP TABLE IF EXISTS fact_touchpoints CASCADE;
DROP TABLE IF EXISTS fact_ad_spend CASCADE;

DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_campaign CASCADE;
DROP TABLE IF EXISTS dim_channel CASCADE;

-- ============================================================
-- DIMENSION TABLES
-- ============================================================

CREATE TABLE dim_channel (
    channel_key SERIAL PRIMARY KEY,
    channel_name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_campaign (
    campaign_key SERIAL PRIMARY KEY,
    campaign_id VARCHAR(100) UNIQUE NOT NULL,
    campaign_name VARCHAR(255),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_number INTEGER,
    week_number INTEGER,
    month_number INTEGER,
    month_name VARCHAR(20),
    quarter_number INTEGER,
    year_number INTEGER
);

-- ============================================================
-- FACT TABLES
-- ============================================================

CREATE TABLE fact_ad_spend (
    ad_spend_key BIGSERIAL PRIMARY KEY,
    campaign_key INTEGER REFERENCES dim_campaign(campaign_key),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    date_key INTEGER REFERENCES dim_date(date_key),
    spend NUMERIC(14,2) DEFAULT 0 CHECK (spend >= 0),
    clicks INTEGER DEFAULT 0 CHECK (clicks >= 0),
    impressions INTEGER DEFAULT 0 CHECK (impressions >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_touchpoints (
    touchpoint_key BIGSERIAL PRIMARY KEY,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    campaign_key INTEGER REFERENCES dim_campaign(campaign_key),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    interaction_time TIMESTAMP NOT NULL,
    touchpoint_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_conversions (
    conversion_key BIGSERIAL PRIMARY KEY,
    conversion_id VARCHAR(100) UNIQUE NOT NULL,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    conversion_date TIMESTAMP NOT NULL,
    revenue NUMERIC(14,2) NOT NULL CHECK (revenue >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_attribution (
    attribution_key BIGSERIAL PRIMARY KEY,
    conversion_key BIGINT REFERENCES fact_conversions(conversion_key),
    touchpoint_key BIGINT REFERENCES fact_touchpoints(touchpoint_key),
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    campaign_key INTEGER REFERENCES dim_campaign(campaign_key),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    attribution_model VARCHAR(50) NOT NULL,
    attribution_weight NUMERIC(12,8) NOT NULL CHECK (attribution_weight >= 0),
    attributed_revenue NUMERIC(14,2) NOT NULL CHECK (attributed_revenue >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- INDEXES FOR QUERY OPTIMIZATION
-- ============================================================

CREATE INDEX idx_dim_channel_name
ON dim_channel(channel_name);

CREATE INDEX idx_dim_campaign_id
ON dim_campaign(campaign_id);

CREATE INDEX idx_dim_customer_user_id
ON dim_customer(user_id);

CREATE INDEX idx_dim_date_full_date
ON dim_date(full_date);

CREATE INDEX idx_fact_ad_spend_channel
ON fact_ad_spend(channel_key);

CREATE INDEX idx_fact_ad_spend_campaign
ON fact_ad_spend(campaign_key);

CREATE INDEX idx_fact_ad_spend_date
ON fact_ad_spend(date_key);

CREATE INDEX idx_fact_touchpoints_customer
ON fact_touchpoints(customer_key);

CREATE INDEX idx_fact_touchpoints_time
ON fact_touchpoints(interaction_time);

CREATE INDEX idx_fact_touchpoints_channel
ON fact_touchpoints(channel_key);

CREATE INDEX idx_fact_conversions_customer
ON fact_conversions(customer_key);

CREATE INDEX idx_fact_conversions_date
ON fact_conversions(conversion_date);

CREATE INDEX idx_fact_attribution_model
ON fact_attribution(attribution_model);

CREATE INDEX idx_fact_attribution_channel
ON fact_attribution(channel_key);

CREATE INDEX idx_fact_attribution_conversion
ON fact_attribution(conversion_key);

-- ============================================================
-- PURPOSE OF THIS SCHEMA
-- ============================================================
-- This schema supports:
-- 1. Customer journey sequencing
-- 2. First touch attribution
-- 3. Last touch attribution
-- 4. Linear attribution
-- 5. Time decay attribution
-- 6. Position based attribution
-- 7. KPI calculation
-- 8. Monthly and weekly trend analysis
-- 9. Dashboard reporting views
-- ============================================================