-- ============================================================
-- MARKETING ATTRIBUTION DASHBOARD
-- DASHBOARD REPORTING VIEWS
-- Developer: Isaac
-- Purpose: Create clean SQL views for Power BI/dashboard reporting
-- ============================================================

SET search_path TO marketing;

-- ============================================================
-- 1. EXECUTIVE SUMMARY VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_executive_summary AS
WITH spend_summary AS (
    SELECT
        SUM(spend) AS total_spend,
        SUM(clicks) AS total_clicks,
        SUM(impressions) AS total_impressions
    FROM fact_ad_spend
),

conversion_summary AS (
    SELECT
        COUNT(DISTINCT conversion_key) AS total_conversions,
        COUNT(DISTINCT customer_key) AS total_customers,
        SUM(revenue) AS total_revenue
    FROM fact_conversions
)

SELECT
    ss.total_spend,
    cs.total_revenue,
    ss.total_clicks,
    ss.total_impressions,
    cs.total_conversions,
    cs.total_customers,

    ss.total_spend /
        NULLIF(ss.total_clicks, 0) AS cpc,

    ss.total_spend /
        NULLIF(ss.total_impressions, 0) * 1000 AS cpm,

    ss.total_spend /
        NULLIF(cs.total_customers, 0) AS cac,

    cs.total_conversions::NUMERIC /
        NULLIF(ss.total_clicks, 0) * 100 AS conversion_rate_percentage,

    cs.total_revenue /
        NULLIF(ss.total_spend, 0) AS roas,

    (
        cs.total_revenue - ss.total_spend
    ) / NULLIF(ss.total_spend, 0) * 100 AS roi_percentage

FROM spend_summary ss
CROSS JOIN conversion_summary cs;

-- ============================================================
-- 2. ATTRIBUTION MODEL COMPARISON VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_attribution_model_comparison AS
SELECT
    fa.attribution_model,
    dc.channel_name,
    COUNT(DISTINCT fa.conversion_key) AS conversion_count,
    ROUND(SUM(fa.attribution_weight), 4) AS conversion_credit,
    ROUND(SUM(fa.attributed_revenue), 2) AS attributed_revenue
FROM fact_attribution fa
JOIN dim_channel dc
    ON dc.channel_key = fa.channel_key
GROUP BY
    fa.attribution_model,
    dc.channel_name;

-- ============================================================
-- 3. CHANNEL ROI VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_channel_roi_by_model AS
WITH channel_spend AS (
    SELECT
        channel_key,
        SUM(spend) AS total_spend,
        SUM(clicks) AS total_clicks,
        SUM(impressions) AS total_impressions
    FROM fact_ad_spend
    GROUP BY channel_key
),

channel_revenue AS (
    SELECT
        channel_key,
        attribution_model,
        SUM(attribution_weight) AS conversion_credit,
        SUM(attributed_revenue) AS attributed_revenue
    FROM fact_attribution
    GROUP BY
        channel_key,
        attribution_model
)

SELECT
    dc.channel_name,
    cr.attribution_model,
    cs.total_spend,
    cs.total_clicks,
    cs.total_impressions,
    cr.conversion_credit,
    cr.attributed_revenue,

    cs.total_spend /
        NULLIF(cs.total_clicks, 0) AS cpc,

    cs.total_spend /
        NULLIF(cs.total_impressions, 0) * 1000 AS cpm,

    cs.total_spend /
        NULLIF(cr.conversion_credit, 0) AS cac,

    cr.attributed_revenue /
        NULLIF(cs.total_spend, 0) AS roas,

    (
        cr.attributed_revenue - cs.total_spend
    ) / NULLIF(cs.total_spend, 0) * 100 AS roi_percentage

FROM channel_spend cs
JOIN dim_channel dc
    ON dc.channel_key = cs.channel_key
LEFT JOIN channel_revenue cr
    ON cr.channel_key = cs.channel_key;

-- ============================================================
-- 4. MONTHLY MARKETING TREND VIEW
-- ============================================================

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

monthly_revenue AS (
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
    mr.attribution_model,
    ms.total_spend,
    ms.total_clicks,
    ms.total_impressions,
    COALESCE(mr.conversion_credit, 0) AS conversion_credit,
    COALESCE(mr.attributed_revenue, 0) AS attributed_revenue,

    ms.total_spend /
        NULLIF(ms.total_clicks, 0) AS cpc,

    ms.total_spend /
        NULLIF(ms.total_impressions, 0) * 1000 AS cpm,

    COALESCE(mr.attributed_revenue, 0) /
        NULLIF(ms.total_spend, 0) AS roas,

    (
        COALESCE(mr.attributed_revenue, 0) - ms.total_spend
    ) / NULLIF(ms.total_spend, 0) * 100 AS roi_percentage

FROM monthly_spend ms
LEFT JOIN monthly_revenue mr
    ON mr.month_start = ms.month_start
   AND mr.channel_name = ms.channel_name;

-- ============================================================
-- 5. WEEKLY MARKETING TREND VIEW
-- ============================================================

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

weekly_revenue AS (
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
    wr.attribution_model,
    ws.total_spend,
    ws.total_clicks,
    ws.total_impressions,
    COALESCE(wr.conversion_credit, 0) AS conversion_credit,
    COALESCE(wr.attributed_revenue, 0) AS attributed_revenue,

    ws.total_spend /
        NULLIF(ws.total_clicks, 0) AS cpc,

    ws.total_spend /
        NULLIF(ws.total_impressions, 0) * 1000 AS cpm,

    COALESCE(wr.attributed_revenue, 0) /
        NULLIF(ws.total_spend, 0) AS roas,

    (
        COALESCE(wr.attributed_revenue, 0) - ws.total_spend
    ) / NULLIF(ws.total_spend, 0) * 100 AS roi_percentage

FROM weekly_spend ws
LEFT JOIN weekly_revenue wr
    ON wr.week_start = ws.week_start
   AND wr.channel_name = ws.channel_name;

-- ============================================================
-- 6. CAMPAIGN PERFORMANCE VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_campaign_performance AS
WITH campaign_spend AS (
    SELECT
        dcamp.campaign_id,
        dcamp.campaign_name,
        dc.channel_name,
        SUM(fas.spend) AS total_spend,
        SUM(fas.clicks) AS total_clicks,
        SUM(fas.impressions) AS total_impressions
    FROM fact_ad_spend fas
    JOIN dim_campaign dcamp
        ON dcamp.campaign_key = fas.campaign_key
    JOIN dim_channel dc
        ON dc.channel_key = fas.channel_key
    GROUP BY
        dcamp.campaign_id,
        dcamp.campaign_name,
        dc.channel_name
),

campaign_revenue AS (
    SELECT
        dcamp.campaign_id,
        fa.attribution_model,
        SUM(fa.attribution_weight) AS conversion_credit,
        SUM(fa.attributed_revenue) AS attributed_revenue
    FROM fact_attribution fa
    JOIN dim_campaign dcamp
        ON dcamp.campaign_key = fa.campaign_key
    GROUP BY
        dcamp.campaign_id,
        fa.attribution_model
)

SELECT
    cs.campaign_id,
    cs.campaign_name,
    cs.channel_name,
    cr.attribution_model,
    cs.total_spend,
    cs.total_clicks,
    cs.total_impressions,
    COALESCE(cr.conversion_credit, 0) AS conversion_credit,
    COALESCE(cr.attributed_revenue, 0) AS attributed_revenue,

    cs.total_spend /
        NULLIF(cs.total_clicks, 0) AS cpc,

    cs.total_spend /
        NULLIF(cs.total_impressions, 0) * 1000 AS cpm,

    COALESCE(cr.attributed_revenue, 0) /
        NULLIF(cs.total_spend, 0) AS roas,

    (
        COALESCE(cr.attributed_revenue, 0) - cs.total_spend
    ) / NULLIF(cs.total_spend, 0) * 100 AS roi_percentage

FROM campaign_spend cs
LEFT JOIN campaign_revenue cr
    ON cr.campaign_id = cs.campaign_id;

-- ============================================================
-- 7. EXECUTIVE SQL SUMMARY BY ATTRIBUTION MODEL
-- ============================================================

CREATE OR REPLACE VIEW vw_executive_sql_summary AS
SELECT
    attribution_model,
    ROUND(SUM(attributed_revenue), 2) AS total_attributed_revenue,
    ROUND(SUM(attribution_weight), 2) AS total_conversion_credit,
    COUNT(DISTINCT conversion_key) AS total_conversions
FROM fact_attribution
GROUP BY attribution_model;

-- ============================================================
-- DASHBOARD VIEWS CREATED
-- ============================================================
-- vw_executive_summary
-- vw_attribution_model_comparison
-- vw_channel_roi_by_model
-- vw_monthly_marketing_trends
-- vw_weekly_marketing_trends
-- vw_campaign_performance
-- vw_executive_sql_summary
-- ============================================================