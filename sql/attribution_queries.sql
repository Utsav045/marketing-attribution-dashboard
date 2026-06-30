-- ============================================================
-- MARKETING ATTRIBUTION DASHBOARD
-- ATTRIBUTION QUERIES
-- Developer: Isaac
-- Purpose: Calculate multiple attribution models using SQL
-- ============================================================

SET search_path TO marketing;

-- ============================================================
-- LOAD DIMENSION TABLES
-- ============================================================

INSERT INTO dim_channel (channel_name)
SELECT DISTINCT channel
FROM (
    SELECT channel FROM stg_ad_spend
    UNION
    SELECT channel FROM stg_customer_journey
) channels
WHERE channel IS NOT NULL
ON CONFLICT (channel_name) DO NOTHING;

INSERT INTO dim_customer (user_id)
SELECT DISTINCT user_id
FROM (
    SELECT user_id FROM stg_customer_journey
    UNION
    SELECT user_id FROM stg_conversions
) customers
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

-- ============================================================
-- LOAD TOUCHPOINT FACT TABLE
-- ============================================================

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
    ON dcamp.campaign_id = sj.campaign_id
WHERE sj.interaction_time IS NOT NULL;

-- ============================================================
-- LOAD CONVERSION FACT TABLE
-- ============================================================

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
WHERE sc.conversion_id IS NOT NULL
  AND sc.conversion_date IS NOT NULL
  AND sc.revenue IS NOT NULL
ON CONFLICT (conversion_id) DO NOTHING;

-- ============================================================
-- FIRST TOUCH ATTRIBUTION
-- 100% credit goes to the first eligible touchpoint
-- ============================================================

DELETE FROM fact_attribution
WHERE attribution_model = 'FIRST_TOUCH';

WITH eligible_touchpoints AS (
    SELECT
        fc.conversion_key,
        fc.customer_key,
        fc.revenue,
        ft.touchpoint_key,
        ft.campaign_key,
        ft.channel_key,
        ROW_NUMBER() OVER (
            PARTITION BY fc.conversion_key
            ORDER BY ft.interaction_time ASC
        ) AS first_touch_rank
    FROM fact_conversions fc
    JOIN fact_touchpoints ft
        ON ft.customer_key = fc.customer_key
       AND ft.interaction_time <= fc.conversion_date
)

INSERT INTO fact_attribution (
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    attribution_model,
    attribution_weight,
    attributed_revenue
)
SELECT
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    'FIRST_TOUCH',
    1.00000000,
    revenue
FROM eligible_touchpoints
WHERE first_touch_rank = 1;

-- ============================================================
-- LAST TOUCH ATTRIBUTION
-- 100% credit goes to the final eligible touchpoint
-- ============================================================

DELETE FROM fact_attribution
WHERE attribution_model = 'LAST_TOUCH';

WITH eligible_touchpoints AS (
    SELECT
        fc.conversion_key,
        fc.customer_key,
        fc.revenue,
        ft.touchpoint_key,
        ft.campaign_key,
        ft.channel_key,
        ROW_NUMBER() OVER (
            PARTITION BY fc.conversion_key
            ORDER BY ft.interaction_time DESC
        ) AS last_touch_rank
    FROM fact_conversions fc
    JOIN fact_touchpoints ft
        ON ft.customer_key = fc.customer_key
       AND ft.interaction_time <= fc.conversion_date
)

INSERT INTO fact_attribution (
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    attribution_model,
    attribution_weight,
    attributed_revenue
)
SELECT
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    'LAST_TOUCH',
    1.00000000,
    revenue
FROM eligible_touchpoints
WHERE last_touch_rank = 1;

-- ============================================================
-- LINEAR ATTRIBUTION
-- Equal credit across all eligible touchpoints
-- ============================================================

DELETE FROM fact_attribution
WHERE attribution_model = 'LINEAR';

WITH eligible_touchpoints AS (
    SELECT
        fc.conversion_key,
        fc.customer_key,
        fc.revenue,
        ft.touchpoint_key,
        ft.campaign_key,
        ft.channel_key,
        COUNT(*) OVER (
            PARTITION BY fc.conversion_key
        ) AS touchpoint_count
    FROM fact_conversions fc
    JOIN fact_touchpoints ft
        ON ft.customer_key = fc.customer_key
       AND ft.interaction_time <= fc.conversion_date
),

linear_weights AS (
    SELECT
        *,
        1.00000000 / NULLIF(touchpoint_count, 0) AS attribution_weight
    FROM eligible_touchpoints
)

INSERT INTO fact_attribution (
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    attribution_model,
    attribution_weight,
    attributed_revenue
)
SELECT
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    'LINEAR',
    attribution_weight,
    revenue * attribution_weight
FROM linear_weights;

-- ============================================================
-- TIME DECAY ATTRIBUTION
-- More credit goes to touchpoints closer to conversion
-- 7-day half life is used
-- ============================================================

DELETE FROM fact_attribution
WHERE attribution_model = 'TIME_DECAY';

WITH eligible_touchpoints AS (
    SELECT
        fc.conversion_key,
        fc.customer_key,
        fc.revenue,
        fc.conversion_date,
        ft.touchpoint_key,
        ft.campaign_key,
        ft.channel_key,
        ft.interaction_time,
        EXTRACT(
            EPOCH FROM (fc.conversion_date - ft.interaction_time)
        ) / 86400 AS days_before_conversion
    FROM fact_conversions fc
    JOIN fact_touchpoints ft
        ON ft.customer_key = fc.customer_key
       AND ft.interaction_time <= fc.conversion_date
),

decay_scores AS (
    SELECT
        *,
        POWER(0.5, days_before_conversion / 7.0) AS decay_score
    FROM eligible_touchpoints
),

time_decay_weights AS (
    SELECT
        *,
        decay_score / NULLIF(
            SUM(decay_score) OVER (
                PARTITION BY conversion_key
            ),
            0
        ) AS attribution_weight
    FROM decay_scores
)

INSERT INTO fact_attribution (
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    attribution_model,
    attribution_weight,
    attributed_revenue
)
SELECT
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    'TIME_DECAY',
    attribution_weight,
    revenue * attribution_weight
FROM time_decay_weights;

-- ============================================================
-- POSITION BASED ATTRIBUTION
-- U-shaped model:
-- 40% first touch, 40% last touch, 20% shared middle
-- ============================================================

DELETE FROM fact_attribution
WHERE attribution_model = 'POSITION_BASED';

WITH eligible_touchpoints AS (
    SELECT
        fc.conversion_key,
        fc.customer_key,
        fc.revenue,
        ft.touchpoint_key,
        ft.campaign_key,
        ft.channel_key,
        ft.interaction_time,

        ROW_NUMBER() OVER (
            PARTITION BY fc.conversion_key
            ORDER BY ft.interaction_time ASC
        ) AS touchpoint_position,

        COUNT(*) OVER (
            PARTITION BY fc.conversion_key
        ) AS total_touchpoints

    FROM fact_conversions fc
    JOIN fact_touchpoints ft
        ON ft.customer_key = fc.customer_key
       AND ft.interaction_time <= fc.conversion_date
),

position_weights AS (
    SELECT
        *,
        CASE
            WHEN total_touchpoints = 1 THEN 1.00000000
            WHEN total_touchpoints = 2 THEN 0.50000000
            WHEN touchpoint_position = 1 THEN 0.40000000
            WHEN touchpoint_position = total_touchpoints THEN 0.40000000
            ELSE 0.20000000 / NULLIF(total_touchpoints - 2, 0)
        END AS attribution_weight
    FROM eligible_touchpoints
)

INSERT INTO fact_attribution (
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    attribution_model,
    attribution_weight,
    attributed_revenue
)
SELECT
    conversion_key,
    touchpoint_key,
    customer_key,
    campaign_key,
    channel_key,
    'POSITION_BASED',
    attribution_weight,
    revenue * attribution_weight
FROM position_weights;

-- ============================================================
-- ATTRIBUTION VALIDATION
-- Each conversion should have total attribution weight of 1.0
-- under each model
-- ============================================================

SELECT
    conversion_key,
    attribution_model,
    ROUND(SUM(attribution_weight), 4) AS total_weight
FROM fact_attribution
GROUP BY
    conversion_key,
    attribution_model
HAVING ROUND(SUM(attribution_weight), 4) <> 1.0000;