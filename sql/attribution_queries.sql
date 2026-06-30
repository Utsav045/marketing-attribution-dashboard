-- First Touch
SELECT
    cookie,
    MIN(timestamp) AS first_touch_time,
    interaction,
    revenue
FROM customer_journeys
WHERE conversion = 1
GROUP BY cookie, interaction, revenue;

-- Last Touch
SELECT
    cookie,
    MAX(timestamp) AS last_touch_time,
    interaction,
    revenue
FROM customer_journeys
WHERE conversion = 1
GROUP BY cookie, interaction, revenue;

-- Linear Attribution
WITH journey_count AS (
    SELECT
        cookie,
        COUNT(*) AS n_touchpoints,
        MAX(revenue) AS total_revenue
    FROM customer_journeys
    WHERE conversion = 1
    GROUP BY cookie
)
SELECT
    cj.cookie,
    cj.interaction,
    jc.total_revenue / jc.n_touchpoints AS attributed_revenue
FROM customer_journeys cj
JOIN journey_count jc
ON cj.cookie = jc.cookie;