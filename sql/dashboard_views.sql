-- Dashboard views for marketing attribution reporting

CREATE OR REPLACE VIEW vw_spend_by_channel AS
SELECT
    channel,
    SUM(spend) AS total_spend,
    SUM(clicks) AS total_clicks,
    SUM(impressions) AS total_impressions
FROM ad_spend_performance
GROUP BY channel;

CREATE OR REPLACE VIEW vw_conversion_summary AS
SELECT
    customer_id,
    COUNT(*) AS conversions,
    SUM(revenue) AS total_revenue
FROM revenue_conversions
GROUP BY customer_id;

CREATE OR REPLACE VIEW vw_campaign_roi AS
SELECT
    a.campaign_id,
    SUM(a.spend) AS total_spend,
    COALESCE(SUM(r.revenue), 0) AS total_revenue,
    CASE
        WHEN SUM(a.spend) = 0 THEN NULL
        ELSE ROUND(COALESCE(SUM(r.revenue), 0) / SUM(a.spend), 2)
    END AS roas
FROM ad_spend_performance a
LEFT JOIN revenue_conversions r
    ON r.campaign_id = a.campaign_id
GROUP BY a.campaign_id;
