-- Attribution queries for customer journey analysis

-- First-touch attribution by customer
WITH ranked_journeys AS (
    SELECT
        customer_id,
        campaign_id,
        touch_order,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY touch_order, interaction_date
        ) AS rn
    FROM customer_journeys
    WHERE converted = TRUE
)
SELECT
    customer_id,
    campaign_id AS first_touch_campaign
FROM ranked_journeys
WHERE rn = 1;

-- Last-touch attribution by customer
WITH ranked_journeys AS (
    SELECT
        customer_id,
        campaign_id,
        touch_order,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY touch_order DESC, interaction_date DESC
        ) AS rn
    FROM customer_journeys
    WHERE converted = TRUE
)
SELECT
    customer_id,
    campaign_id AS last_touch_campaign
FROM ranked_journeys
WHERE rn = 1;
