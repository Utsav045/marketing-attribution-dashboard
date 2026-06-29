SET search_path TO marketing;

SELECT
    conversion_key,
    attribution_model,
    ROUND(SUM(attribution_weight), 4) AS total_weight
FROM fact_attribution
GROUP BY
    conversion_key,
    attribution_model
HAVING ROUND(SUM(attribution_weight), 4) <> 1.0000;

SELECT
    fa.conversion_key,
    fa.attribution_model,
    ROUND(fc.revenue, 2) AS original_revenue,
    ROUND(SUM(fa.attributed_revenue), 2) AS allocated_revenue,
    ROUND(fc.revenue - SUM(fa.attributed_revenue), 2) AS difference
FROM fact_attribution fa
JOIN fact_conversions fc
    ON fc.conversion_key = fa.conversion_key
GROUP BY
    fa.conversion_key,
    fa.attribution_model,
    fc.revenue
HAVING ABS(fc.revenue - SUM(fa.attributed_revenue)) > 0.01;

SELECT
    conversion_key,
    touchpoint_key,
    attribution_model,
    COUNT(*) AS duplicate_count
FROM fact_attribution
GROUP BY
    conversion_key,
    touchpoint_key,
    attribution_model
HAVING COUNT(*) > 1;

SELECT
    touchpoint_key
FROM fact_touchpoints
WHERE channel_key IS NULL;

SELECT
    conversion_key
FROM fact_conversions fc
WHERE NOT EXISTS (
    SELECT 1
    FROM fact_attribution fa
    WHERE fa.conversion_key = fc.conversion_key
);