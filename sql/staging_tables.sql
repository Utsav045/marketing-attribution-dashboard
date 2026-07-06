-- Staging tables for raw marketing data sources

CREATE TABLE IF NOT EXISTS stg_ad_spend (
    spend_id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(50),
    channel VARCHAR(100),
    spend DECIMAL(14,2) DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    spend_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_customer_journey (
    journey_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    cookie VARCHAR(100),
    channel VARCHAR(100),
    campaign_id VARCHAR(50),
    interaction_time TIMESTAMP,
    interaction VARCHAR(150),
    conversion SMALLINT DEFAULT 0,
    revenue DECIMAL(14,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stg_conversions (
    conversion_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50),
    revenue DECIMAL(14,2) DEFAULT 0,
    conversion_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
