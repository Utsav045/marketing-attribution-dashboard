-- Core schema for the marketing attribution dashboard

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(150) NOT NULL,
    channel VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(150),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customer_journeys (
    journey_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    campaign_id INTEGER NOT NULL REFERENCES campaigns(campaign_id),
    interaction_date DATE NOT NULL,
    touch_order INTEGER NOT NULL,
    converted BOOLEAN DEFAULT FALSE,
    revenue DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ad_spend_performance (
    spend_id SERIAL PRIMARY KEY,
    campaign_id INTEGER NOT NULL REFERENCES campaigns(campaign_id),
    channel VARCHAR(100) NOT NULL,
    spend DECIMAL(12,2) DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    spend_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS revenue_conversions (
    conversion_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    campaign_id INTEGER NOT NULL REFERENCES campaigns(campaign_id),
    revenue DECIMAL(12,2) DEFAULT 0,
    conversion_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_customer_journeys_customer_id ON customer_journeys(customer_id);
CREATE INDEX IF NOT EXISTS idx_customer_journeys_campaign_id ON customer_journeys(campaign_id);
CREATE INDEX IF NOT EXISTS idx_customer_journeys_interaction_date ON customer_journeys(interaction_date);
CREATE INDEX IF NOT EXISTS idx_spend_campaign ON ad_spend_performance(campaign_id);
