SET search_path TO marketing;

CREATE OR REPLACE VIEW vw_monthly_marketing_trends AS
WITH monthly_spend AS (
    SELECT
        DATE_TRUNC('month', dd.full_date)::DATE AS month_start,
        dc.channel_name,
        SUM(fas.spend) AS total_spend,
        SUM(fas.clicks) AS total_clicks,
        SUM(fas.impressions) AS total_impressions
    FROM fact_ad_spend fas
    JOIN dim_date dd
        ON dd.date_key = fas.date_key
    JOIN dim_channel dc
        ON dc.channel_key = fas.channel_key
    GROUP BY
        DATE_TRUNC('month', dd.full_date),
        dc.channel_name
),

monthly_attribution AS (
    SELECT
        DATE_TRUNC('month', fc.conversion_date)::DATE AS month_start,
        dc.channel_name,
        fa.attribution_model,
        SUM(fa.attribution_weight) AS conversion_credit,
        SUM(fa.attributed_revenue) AS attributed_revenue
    FROM fact_attribution fa
    JOIN fact_conversions fc
        ON fc.conversion_key = fa.conversion_key
    JOIN dim_channel dc
        ON dc.channel_key = fa.channel_key
    GROUP BY
        DATE_TRUNC('month', fc.conversion_date),
        dc.channel_name,
        fa.attribution_model
)

SELECT
    ms.month_start,
    ms.channel_name,
    ma.attribution_model,
    ms.total_spend,
    ms.total_clicks,
    ms.total_impressions,
    COALESCE(ma.conversion_credit, 0) AS conversion_credit,
    COALESCE(ma.attributed_revenue, 0) AS attributed_revenue,
    ms.total_spend / NULLIF(ms.total_clicks, 0) AS cpc,
    ms.total_spend / NULLIF(ms.total_impressions, 0) * 1000 AS cpm,
    COALESCE(ma.attributed_revenue, 0) / NULLIF(ms.total_spend, 0) AS roas,
    (
        COALESCE(ma.attributed_revenue, 0) - ms.total_spend
    ) / NULLIF(ms.total_spend, 0) * 100 AS roi_percentage
FROM monthly_spend ms
LEFT JOIN monthly_attribution ma
    ON ma.month_start = ms.month_start
   AND ma.channel_name = ms.channel_name;

CREATE OR REPLACE VIEW vw_weekly_marketing_trends AS
WITH weekly_spend AS (
    SELECT
        DATE_TRUNC('week', dd.full_date)::DATE AS week_start,
        dc.channel_name,
        SUM(fas.spend) AS total_spend,
        SUM(fas.clicks) AS total_clicks,
        SUM(fas.impressions) AS total_impressions
    FROM fact_ad_spend fas
    JOIN dim_date dd
        ON dd.date_key = fas.date_key
    JOIN dim_channel dc
        ON dc.channel_key = fas.channel_key
    GROUP BY
        DATE_TRUNC('week', dd.full_date),
        dc.channel_name
),

weekly_attribution AS (
    SELECT
        DATE_TRUNC('week', fc.conversion_date)::DATE AS week_start,
        dc.channel_name,
        fa.attribution_model,
        SUM(fa.attribution_weight) AS conversion_credit,
        SUM(fa.attributed_revenue) AS attributed_revenue
    FROM fact_attribution fa
    JOIN fact_conversions fc
        ON fc.conversion_key = fa.conversion_key
    JOIN dim_channel dc
        ON dc.channel_key = fa.channel_key
    GROUP BY
        DATE_TRUNC('week', fc.conversion_date),
        dc.channel_name,
        fa.attribution_model
)

SELECT
    ws.week_start,
    ws.channel_name,
    wa.attribution_model,
    ws.total_spend,
    ws.total_clicks,
    ws.total_impressions,
    COALESCE(wa.conversion_credit, 0) AS conversion_credit,
    COALESCE(wa.attributed_revenue, 0) AS attributed_revenue,
    ws.total_spend / NULLIF(ws.total_clicks, 0) AS cpc,
    ws.total_spend / NULLIF(ws.total_impressions, 0) * 1000 AS cpm,
    COALESCE(wa.attributed_revenue, 0) / NULLIF(ws.total_spend, 0) AS roas,
    (
        COALESCE(wa.attributed_revenue, 0) - ws.total_spend
    ) / NULLIF(ws.total_spend, 0) * 100 AS roi_percentage
FROM weekly_spend ws
LEFT JOIN weekly_attribution wa
    ON wa.week_start = ws.week_start
   AND wa.channel_name = ws.channel_name;