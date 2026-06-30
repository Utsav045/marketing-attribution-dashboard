-- ============================================================
-- MARKETING ATTRIBUTION DASHBOARD
-- STAGING TABLES
-- Developer: Isaac
-- Purpose: Store raw marketing datasets before transformation
-- ============================================================

CREATE SCHEMA IF NOT EXISTS marketing;

SET search_path TO marketing;

-- ============================================================
-- DROP STAGING TABLES DURING DEVELOPMENT
-- ============================================================

DROP TABLE IF EXISTS stg_ad_spend CASCADE;
DROP TABLE IF EXISTS stg_customer_journey CASCADE;
DROP TABLE IF EXISTS stg_conversions CASCADE;

-- ============================================================
-- AD SPEND STAGING TABLE
-- ============================================================

CREATE TABLE stg_ad_spend (
    campaign_id VARCHAR(100),
    channel VARCHAR(100),
    spend NUMERIC(14,2),
    clicks INTEGER,
    impressions INTEGER,
    spend_date DATE,
    source_file VARCHAR(255),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CUSTOMER JOURNEY STAGING TABLE
-- ============================================================

CREATE TABLE stg_customer_journey (
    journey_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    channel VARCHAR(100),
    interaction_time TIMESTAMP,
    campaign_id VARCHAR(100),
    source_file VARCHAR(255),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CONVERSIONS STAGING TABLE
-- ============================================================

CREATE TABLE stg_conversions (
    conversion_id VARCHAR(100),
    user_id VARCHAR(100),
    revenue NUMERIC(14,2),
    conversion_date TIMESTAMP,
    source_file VARCHAR(255),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- BASIC DATA QUALITY CHECKS
-- ============================================================

-- Missing campaign ID in ad spend
SELECT
    'missing_campaign_id_ad_spend' AS check_name,
    COUNT(*) AS issue_count
FROM stg_ad_spend
WHERE campaign_id IS NULL;

-- Missing user ID in customer journey
SELECT
    'missing_user_id_customer_journey' AS check_name,
    COUNT(*) AS issue_count
FROM stg_customer_journey
WHERE user_id IS NULL;

-- Missing conversion ID
SELECT
    'missing_conversion_id' AS check_name,
    COUNT(*) AS issue_count
FROM stg_conversions
WHERE conversion_id IS NULL;

-- Missing revenue
SELECT
    'missing_revenue' AS check_name,
    COUNT(*) AS issue_count
FROM stg_conversions
WHERE revenue IS NULL;

-- Negative spend
SELECT
    'negative_spend' AS check_name,
    COUNT(*) AS issue_count
FROM stg_ad_spend
WHERE spend < 0;

-- Negative revenue
SELECT
    'negative_revenue' AS check_name,
    COUNT(*) AS issue_count
FROM stg_conversions
WHERE revenue < 0;

-- ============================================================
-- CHANNEL STANDARDIZATION
-- ============================================================

UPDATE stg_ad_spend
SET channel = LOWER(TRIM(channel))
WHERE channel IS NOT NULL;

UPDATE stg_customer_journey
SET channel = LOWER(TRIM(channel))
WHERE channel IS NOT NULL;

UPDATE stg_ad_spend
SET channel =
    CASE
        WHEN channel IN ('fb', 'facebook ads', 'meta', 'meta ads') THEN 'facebook'
        WHEN channel IN ('google ads', 'google search', 'adwords') THEN 'google'
        WHEN channel IN ('email marketing', 'email campaign') THEN 'email'
        WHEN channel IN ('linkedin ads', 'linkedin') THEN 'linkedin'
        WHEN channel IN ('instagram ads', 'instagram') THEN 'instagram'
        WHEN channel IN ('youtube ads', 'youtube') THEN 'youtube'
        ELSE channel
    END;

UPDATE stg_customer_journey
SET channel =
    CASE
        WHEN channel IN ('fb', 'facebook ads', 'meta', 'meta ads') THEN 'facebook'
        WHEN channel IN ('google ads', 'google search', 'adwords') THEN 'google'
        WHEN channel IN ('email marketing', 'email campaign') THEN 'email'
        WHEN channel IN ('linkedin ads', 'linkedin') THEN 'linkedin'
        WHEN channel IN ('instagram ads', 'instagram') THEN 'instagram'
        WHEN channel IN ('youtube ads', 'youtube') THEN 'youtube'
        ELSE channel
    END;

-- ============================================================
-- DUPLICATE CHECKS
-- ============================================================

SELECT
    conversion_id,
    COUNT(*) AS duplicate_count
FROM stg_conversions
GROUP BY conversion_id
HAVING COUNT(*) > 1;

SELECT
    user_id,
    channel,
    interaction_time,
    campaign_id,
    COUNT(*) AS duplicate_count
FROM stg_customer_journey
GROUP BY
    user_id,
    channel,
    interaction_time,
    campaign_id
HAVING COUNT(*) > 1;

-- ============================================================
-- PURPOSE OF STAGING TABLES
-- ============================================================
-- These staging tables allow raw marketing datasets to be loaded
-- before transformation into analytical dimension and fact tables.
-- ============================================================