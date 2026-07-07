-- KPI queries for campaign and channel performance

SELECT
    channel,
    SUM(spend) AS total_spend,
    SUM(clicks) AS total_clicks,
    SUM(impressions) AS total_impressions
FROM ad_spend_performance
GROUP BY channel;

SELECT
    campaign_id,
    SUM(spend) AS total_spend,
    COALESCE(SUM(revenue), 0) AS total_revenue,
    CASE
        WHEN SUM(spend) = 0 THEN NULL
        ELSE ROUND(COALESCE(SUM(revenue), 0) / SUM(spend), 2)
    END AS roas
FROM (
    SELECT
        a.campaign_id,
        a.spend,
        r.revenue
    FROM ad_spend_performance a
    LEFT JOIN revenue_conversions r
        ON a.campaign_id = r.campaign_id
) x
GROUP BY campaign_id;
