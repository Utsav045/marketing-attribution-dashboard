-- ============================================================
-- MARKETING ATTRIBUTION DASHBOARD
-- KPI CALCULATION QUERIES
-- Developer: Isaac
-- Purpose: Calculate marketing KPIs for attribution reporting
-- ============================================================

SET search_path TO marketing;

-- ============================================================
-- 1. TOTAL SPEND
-- ============================================================

SELECT
    SUM(spend) AS total_spend
FROM fact_ad_spend;

-- ============================================================
-- 2. TOTAL REVENUE
-- ============================================================

SELECT
    SUM(revenue) AS total_revenue
FROM fact_conversions;

-- ============================================================
-- 3. TOTAL CLICKS AND IMPRESSIONS
-- ============================================================

SELECT
    SUM(clicks) AS total_clicks,
    SUM(impressions) AS total_impressions
FROM fact_ad_spend;

-- ============================================================
-- 4. COST PER CLICK
-- CPC = Total Spend / Total Clicks
-- ============================================================

SELECT
    SUM(spend) / NULLIF(SUM(clicks), 0) AS cpc
FROM fact_ad_spend;

-- ============================================================
-- 5. COST PER THOUSAND IMPRESSIONS
-- CPM = Total Spend / Total Impressions * 1000
-- ============================================================

SELECT
    SUM(spend) / NULLIF(SUM(impressions), 0) * 1000 AS cpm
FROM fact_ad_spend;

-- ============================================================
-- 6. CUSTOMER ACQUISITION COST
-- CAC = Total Spend / Number of Converting Customers
-- ============================================================

WITH spend_total AS (
    SELECT
        SUM(spend) AS total_spend
    FROM fact_ad_spend
),

customer_total AS (
    SELECT
        COUNT(DISTINCT customer_key) AS acquired_customers
    FROM fact_conversions
)

SELECT
    st.total_spend / NULLIF(ct.acquired_customers, 0) AS cac
FROM spend_total st
CROSS JOIN customer_total ct;

-- ============================================================
-- 7. CONVERSION RATE
-- Conversion Rate = Total Conversions / Total Clicks * 100
-- ============================================================

WITH click_total AS (
    SELECT
        SUM(clicks) AS total_clicks
    FROM fact_ad_spend
),

conversion_total AS (
    SELECT
        COUNT(DISTINCT conversion_key) AS total_conversions
    FROM fact_conversions
)

SELECT
    ct.total_conversions::NUMERIC /
    NULLIF(cl.total_clicks, 0) * 100 AS conversion_rate_percentage
FROM conversion_total ct
CROSS JOIN click_total cl;

-- ============================================================
-- 8. RETURN ON AD SPEND
-- ROAS = Attributed Revenue / Total Spend
-- ============================================================

WITH spend_total AS (
    SELECT
        SUM(spend) AS total_spend
    FROM fact_ad_spend
),

revenue_total AS (
    SELECT
        attribution_model,
        SUM(attributed_revenue) AS attributed_revenue
    FROM fact_attribution
    GROUP BY attribution_model
)

SELECT
    rt.attribution_model,
    rt.attributed_revenue,
    st.total_spend,
    rt.attributed_revenue / NULLIF(st.total_spend, 0) AS roas
FROM revenue_total rt
CROSS JOIN spend_total st
ORDER BY roas DESC;

-- ============================================================
-- 9. RETURN ON INVESTMENT
-- ROI = (Attributed Revenue - Total Spend) / Total Spend * 100
-- ============================================================

WITH spend_total AS (
    SELECT
        SUM(spend) AS total_spend
    FROM fact_ad_spend
),

revenue_total AS (
    SELECT
        attribution_model,
        SUM(attributed_revenue) AS attributed_revenue
    FROM fact_attribution
    GROUP BY attribution_model
)

SELECT
    rt.attribution_model,
    rt.attributed_revenue,
    st.total_spend,
    (
        rt.attributed_revenue - st.total_spend
    ) / NULLIF(st.total_spend, 0) * 100 AS roi_percentage
FROM revenue_total rt
CROSS JOIN spend_total st
ORDER BY roi_percentage DESC;

-- ============================================================
-- 10. REVENUE PER CUSTOMER
-- ============================================================

SELECT
    SUM(revenue) /
    NULLIF(COUNT(DISTINCT customer_key), 0) AS revenue_per_customer
FROM fact_conversions;

-- ============================================================
-- 11. CHANNEL LEVEL KPI SUMMARY
-- ============================================================

WITH channel_spend AS (
    SELECT
        dc.channel_name,
        SUM(fas.spend) AS total_spend,
        SUM(fas.clicks) AS total_clicks,
        SUM(fas.impressions) AS total_impressions
    FROM fact_ad_spend fas
    JOIN dim_channel dc
        ON dc.channel_key = fas.channel_key
    GROUP BY dc.channel_name
),

channel_revenue AS (
    SELECT
        dc.channel_name,
        fa.attribution_model,
        SUM(fa.attribution_weight) AS conversion_credit,
        SUM(fa.attributed_revenue) AS attributed_revenue
    FROM fact_attribution fa
    JOIN dim_channel dc
        ON dc.channel_key = fa.channel_key
    GROUP BY
        dc.channel_name,
        fa.attribution_model
)

SELECT
    cs.channel_name,
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
LEFT JOIN channel_revenue cr
    ON cr.channel_name = cs.channel_name
ORDER BY
    cr.attribution_model,
    roas DESC;

-- ============================================================
-- 12. CAMPAIGN LEVEL KPI SUMMARY
-- ============================================================

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
    cr.conversion_credit,
    cr.attributed_revenue,

    cs.total_spend /
        NULLIF(cs.total_clicks, 0) AS cpc,

    cs.total_spend /
        NULLIF(cs.total_impressions, 0) * 1000 AS cpm,

    cr.attributed_revenue /
        NULLIF(cs.total_spend, 0) AS roas,

    (
        cr.attributed_revenue - cs.total_spend
    ) / NULLIF(cs.total_spend, 0) * 100 AS roi_percentage

FROM campaign_spend cs
LEFT JOIN campaign_revenue cr
    ON cr.campaign_id = cs.campaign_id
ORDER BY
    cr.attribution_model,
    roas DESC;

-- ============================================================
-- 13. EXECUTIVE KPI SUMMARY
-- ============================================================

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