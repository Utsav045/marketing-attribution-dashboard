SET search_path TO marketing;

SELECT
    'ad_spend_missing_campaign' AS check_name,
    COUNT(*) AS issue_count
FROM stg_ad_spend
WHERE campaign_id IS NULL;

SELECT
    'journey_missing_user' AS check_name,
    COUNT(*) AS issue_count
FROM stg_customer_journey
WHERE user_id IS NULL;

SELECT
    'conversion_missing_revenue' AS check_name,
    COUNT(*) AS issue_count
FROM stg_conversions
WHERE revenue IS NULL;

SELECT
    channel,
    COUNT(*) AS total_records
FROM stg_customer_journey
GROUP BY channel
ORDER BY total_records DESC;

UPDATE stg_ad_spend
SET channel = LOWER(TRIM(channel));

UPDATE stg_customer_journey
SET channel = LOWER(TRIM(channel));

UPDATE stg_customer_journey
SET channel =
    CASE
        WHEN channel IN ('fb', 'facebook ads', 'meta', 'meta ads') THEN 'facebook'
        WHEN channel IN ('google ads', 'google search', 'adwords') THEN 'google'
        WHEN channel IN ('email marketing', 'email campaign') THEN 'email'
        WHEN channel IN ('linkedin ads', 'linkedin') THEN 'linkedin'
        WHEN channel IN ('instagram ads', 'instagram') THEN 'instagram'
        ELSE channel
    END;