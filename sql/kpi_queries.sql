-- Total Revenue
SELECT
    SUM(revenue) AS total_revenue
FROM revenue_conversions;

-- Total Ad Spend
SELECT
    SUM(spend) AS total_spend
FROM ad_spend_performance;

-- ROAS
SELECT
(
    (SELECT SUM(revenue) FROM revenue_conversions)
    /
    NULLIF((SELECT SUM(spend) FROM ad_spend_performance),0)
) AS roas;

-- ROI
SELECT
(
(
    (SELECT SUM(revenue) FROM revenue_conversions)
    -
    (SELECT SUM(spend) FROM ad_spend_performance)
)
/
NULLIF((SELECT SUM(spend) FROM ad_spend_performance),0)
) * 100 AS roi_percentage;

-- Conversion Rate
SELECT
ROUND(
(COUNT(*) FILTER (WHERE conversion = 1)::DECIMAL
/
COUNT(*))*100,
2
) AS conversion_rate
FROM customer_journeys;

-- Spend by Channel
SELECT
channel,
SUM(spend) AS total_spend
FROM ad_spend_performance
GROUP BY channel
ORDER BY total_spend DESC;

-- Average Revenue Per Conversion
SELECT
AVG(revenue) AS average_revenue
FROM revenue_conversions;

-- Highest Spend Channel
SELECT
channel,
SUM(spend) AS total_spend
FROM ad_spend_performance
GROUP BY channel
ORDER BY total_spend DESC
LIMIT 1;

-- Duplicate Cookie Check
SELECT
cookie,
COUNT(*) AS occurrences
FROM customer_journeys
GROUP BY cookie
HAVING COUNT(*) > 1;

-- NULL Value Check
SELECT *
FROM customer_journeys
WHERE
cookie IS NULL
OR timestamp IS NULL
OR interaction IS NULL;