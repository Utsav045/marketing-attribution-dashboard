-- Create Table customer_journeys
CREATE TABLE customer_journeys (
    journey_id SERIAL PRIMARY KEY,
    cookie VARCHAR(100) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    interaction VARCHAR(100),
    conversion SMALLINT DEFAULT 0,
    revenue DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Table campaigns
CREATE TABLE campaigns (
    campaign_id VARCHAR(50) PRIMARY KEY,
    campaign_name VARCHAR(200),
    channels_used VARCHAR(200),
    duration_days INTEGER,
    clicks BIGINT DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    acquisition_cost DECIMAL(14,2),
    roi_pct DECIMAL(8,2),
    location VARCHAR(100),
    language VARCHAR(50)
);

-- Ad Spend Performance Table
CREATE TABLE ad_spend_performance (
    spend_id SERIAL PRIMARY KEY,
    campaign_id VARCHAR(50),
    channel VARCHAR(100) NOT NULL,
    spend DECIMAL(14,2) DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    spend_date DATE NOT NULL
);

-- Revenue / Conversions Table
CREATE TABLE revenue_conversions (
   conversion_id VARCHAR(50) PRIMARY KEY,
   user_id VARCHAR(50) NOT NULL,
   revenue DECIMAL(12,2) DEFAULT 0,
   conversion_date VARCHAR(50)  -- CSV mein date string format (DD-MM-YYYY) mein hai
);

-- Create Indexs
CREATE INDEX idx_journeys_cookie
ON customer_journeys(cookie);

CREATE INDEX idx_spend_campaign
ON ad_spend_performance(campaign_id);

CREATE INDEX idx_revenue_user
ON revenue_conversions(user_id);

-- Check index
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public';