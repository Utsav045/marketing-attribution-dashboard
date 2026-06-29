SET search_path TO marketing;

CREATE OR REPLACE VIEW vw_attribution_model_comparison AS
SELECT
    fa.attribution_model,
    dc.channel_name,
    ROUND(SUM(fa.attribution_weight), 2) AS conversion_credit,
    ROUND(SUM(fa.attributed_revenue), 2) AS attributed_revenue,
    COUNT(DISTINCT fa.conversion_key) AS conversion_count
FROM fact_attribution fa
JOIN dim_channel dc
    ON dc.channel_key = fa.channel_key
GROUP BY
    fa.attribution_model,
    dc.channel_name;

CREATE OR REPLACE VIEW vw_channel_roi_by_model AS
WITH spend_data AS (
    SELECT
        channel_key,
        SUM(spend) AS total_spend,
        SUM(clicks) AS total_clicks,
        SUM(impressions) AS total_impressions
    FROM fact_ad_spend
    GROUP BY channel_key
),

revenue_data AS (
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
    rd.attribution_model,
    sd.total_spend,
    sd.total_clicks,
    sd.total_impressions,
    rd.conversion_credit,
    rd.attributed_revenue,
    sd.total_spend / NULLIF(sd.total_clicks, 0) AS cpc,
    sd.total_spend / NULLIF(sd.total_impressions, 0) * 1000 AS cpm,
    sd.total_spend / NULLIF(rd.conversion_credit, 0) AS cac,
    rd.attributed_revenue / NULLIF(sd.total_spend, 0) AS roas,
    (
        rd.attributed_revenue - sd.total_spend
    ) / NULLIF(sd.total_spend, 0) * 100 AS roi_percentage
FROM revenue_data rd
JOIN spend_data sd
    ON sd.channel_key = rd.channel_key
JOIN dim_channel dc
    ON dc.channel_key = rd.channel_key;

CREATE OR REPLACE VIEW vw_executive_sql_summary AS
SELECT
    attribution_model,
    ROUND(SUM(attributed_revenue), 2) AS total_attributed_revenue,
    ROUND(SUM(attribution_weight), 2) AS total_conversion_credit,
    COUNT(DISTINCT conversion_key) AS total_conversions
FROM fact_attribution
GROUP BY attribution_model;