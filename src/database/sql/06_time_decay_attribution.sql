SET search_path TO marketing;

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

final_weights AS (
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
FROM final_weights;