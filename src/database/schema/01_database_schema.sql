CREATE SCHEMA IF NOT EXISTS marketing;

SET search_path TO marketing;

CREATE TABLE IF NOT EXISTS stg_ad_spend (
    campaign_id VARCHAR(100),
    channel VARCHAR(100),
    spend NUMERIC(14,2),
    clicks INTEGER,
    impressions INTEGER,
    spend_date DATE
);

CREATE TABLE IF NOT EXISTS stg_customer_journey (
    journey_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    channel VARCHAR(100),
    interaction_time TIMESTAMP,
    campaign_id VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS stg_conversions (
    conversion_id VARCHAR(100),
    user_id VARCHAR(100),
    revenue NUMERIC(14,2),
    conversion_date TIMESTAMP
);