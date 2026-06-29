SET search_path TO marketing;

INSERT INTO dim_channel (channel_name)
SELECT DISTINCT channel
FROM (
    SELECT channel FROM stg_ad_spend
    UNION
    SELECT channel FROM stg_customer_journey
) all_channels
WHERE channel IS NOT NULL
ON CONFLICT (channel_name) DO NOTHING;

INSERT INTO dim_customer (user_id)
SELECT DISTINCT user_id
FROM (
    SELECT user_id FROM stg_customer_journey
    UNION
    SELECT user_id FROM stg_conversions
) all_customers
WHERE user_id IS NOT NULL
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO dim_campaign (
    campaign_id,
    campaign_name,
    channel_key
)
SELECT DISTINCT
    s.campaign_id,
    s.campaign_id AS campaign_name,
    c.channel_key
FROM stg_ad_spend s
JOIN dim_channel c
    ON c.channel_name = s.channel
WHERE s.campaign_id IS NOT NULL
ON CONFLICT (campaign_id) DO NOTHING;

INSERT INTO fact_touchpoints (
    customer_key,
    campaign_key,
    channel_key,
    interaction_time,
    touchpoint_order
)
SELECT
    dc.customer_key,
    dcamp.campaign_key,
    dch.channel_key,
    sj.interaction_time,
    ROW_NUMBER() OVER (
        PARTITION BY sj.user_id
        ORDER BY sj.interaction_time
    ) AS touchpoint_order
FROM stg_customer_journey sj
JOIN dim_customer dc
    ON dc.user_id = sj.user_id
JOIN dim_channel dch
    ON dch.channel_name = sj.channel
LEFT JOIN dim_campaign dcamp
    ON dcamp.campaign_id = sj.campaign_id;

INSERT INTO fact_conversions (
    conversion_id,
    customer_key,
    conversion_date,
    revenue
)
SELECT
    sc.conversion_id,
    dc.customer_key,
    sc.conversion_date,
    sc.revenue
FROM stg_conversions sc
JOIN dim_customer dc
    ON dc.user_id = sc.user_id
ON CONFLICT (conversion_id) DO NOTHING;