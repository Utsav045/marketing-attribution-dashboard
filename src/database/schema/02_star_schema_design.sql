SET search_path TO marketing;

CREATE TABLE IF NOT EXISTS dim_channel (
    channel_key SERIAL PRIMARY KEY,
    channel_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_campaign (
    campaign_key SERIAL PRIMARY KEY,
    campaign_id VARCHAR(100) UNIQUE NOT NULL,
    campaign_name VARCHAR(255),
    channel_key INTEGER REFERENCES dim_channel(channel_key)
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_number INTEGER,
    week_number INTEGER,
    month_number INTEGER,
    month_name VARCHAR(20),
    quarter_number INTEGER,
    year_number INTEGER
);

CREATE TABLE IF NOT EXISTS fact_ad_spend (
    ad_spend_key BIGSERIAL PRIMARY KEY,
    campaign_key INTEGER REFERENCES dim_campaign(campaign_key),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    date_key INTEGER REFERENCES dim_date(date_key),
    spend NUMERIC(14,2) DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fact_touchpoints (
    touchpoint_key BIGSERIAL PRIMARY KEY,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    campaign_key INTEGER REFERENCES dim_campaign(campaign_key),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    interaction_time TIMESTAMP NOT NULL,
    touchpoint_order INTEGER
);

CREATE TABLE IF NOT EXISTS fact_conversions (
    conversion_key BIGSERIAL PRIMARY KEY,
    conversion_id VARCHAR(100) UNIQUE NOT NULL,
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    conversion_date TIMESTAMP NOT NULL,
    revenue NUMERIC(14,2) NOT NULL CHECK (revenue >= 0)
);

CREATE TABLE IF NOT EXISTS fact_attribution (
    attribution_key BIGSERIAL PRIMARY KEY,
    conversion_key BIGINT REFERENCES fact_conversions(conversion_key),
    touchpoint_key BIGINT REFERENCES fact_touchpoints(touchpoint_key),
    customer_key INTEGER REFERENCES dim_customer(customer_key),
    campaign_key INTEGER REFERENCES dim_campaign(campaign_key),
    channel_key INTEGER REFERENCES dim_channel(channel_key),
    attribution_model VARCHAR(50) NOT NULL,
    attribution_weight NUMERIC(12,8) NOT NULL,
    attributed_revenue NUMERIC(14,2) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fact_touchpoints_customer
ON fact_touchpoints(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_touchpoints_time
ON fact_touchpoints(interaction_time);

CREATE INDEX IF NOT EXISTS idx_fact_conversions_customer
ON fact_conversions(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_attribution_model
ON fact_attribution(attribution_model);

CREATE INDEX IF NOT EXISTS idx_fact_attribution_channel
ON fact_attribution(channel_key);