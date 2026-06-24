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