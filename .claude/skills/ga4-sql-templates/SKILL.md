# GA4 SQL Templates

Reusable BigQuery SQL queries for GA4 analysis. All queries target `zipmend-2e643.analytics_287815421`.

Replace `{START_DATE}` and `{END_DATE}` with `YYYYMMDD` format dates.

---

## Sessions

```sql
-- Session count, users, and engagement by date
SELECT
  event_date,
  COUNT(DISTINCT CONCAT(user_pseudo_id, (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id'))) AS sessions,
  COUNT(DISTINCT user_pseudo_id) AS users,
  SUM((SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'engagement_time_msec')) / 1000.0 AS total_engagement_sec
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
GROUP BY event_date
ORDER BY event_date
```

## Conversions (Purchases)

```sql
-- Purchase events with revenue, items, and route
SELECT
  event_date,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id') AS transaction_id,
  user_id,
  ecommerce.purchase_revenue AS revenue,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'currency') AS currency,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'payment_type') AS payment_type,
  ARRAY_LENGTH(items) AS item_count
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
  AND event_name = 'purchase'
ORDER BY event_date DESC
```

## Attribution (Traffic Sources)

```sql
-- Sessions by source/medium with conversion rate
WITH sessions AS (
  SELECT
    CONCAT(user_pseudo_id, (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id')) AS session_id,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'source') AS source,
    (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'medium') AS medium,
    MAX(IF(event_name = 'purchase', 1, 0)) AS converted
  FROM `zipmend-2e643.analytics_287815421.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
  GROUP BY session_id, source, medium
)
SELECT
  IFNULL(source, '(direct)') AS source,
  IFNULL(medium, '(none)') AS medium,
  COUNT(*) AS sessions,
  SUM(converted) AS conversions,
  SAFE_DIVIDE(SUM(converted), COUNT(*)) AS conversion_rate
FROM sessions
GROUP BY source, medium
ORDER BY sessions DESC
```

## Event Parameters

```sql
-- List all event parameter keys and their frequency for a given event
SELECT
  ep.key,
  COUNT(*) AS occurrences,
  COUNTIF(ep.value.string_value IS NOT NULL) AS string_values,
  COUNTIF(ep.value.int_value IS NOT NULL) AS int_values,
  COUNTIF(ep.value.float_value IS NOT NULL) AS float_values
FROM `zipmend-2e643.analytics_287815421.events_*`, UNNEST(event_params) AS ep
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
  AND event_name = '{EVENT_NAME}'
GROUP BY ep.key
ORDER BY occurrences DESC
```

## Ecommerce

```sql
-- Daily revenue, transactions, and AOV
SELECT
  event_date,
  COUNT(DISTINCT (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id')) AS transactions,
  SUM(ecommerce.purchase_revenue) AS revenue,
  SAFE_DIVIDE(SUM(ecommerce.purchase_revenue), COUNT(DISTINCT (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'transaction_id'))) AS aov
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
  AND event_name = 'purchase'
GROUP BY event_date
ORDER BY event_date
```

## Event Counts by Name

```sql
-- All events ranked by frequency
SELECT event_name, COUNT(*) AS cnt
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
GROUP BY event_name
ORDER BY cnt DESC
```

## Validate Tag Firing

```sql
-- Check if a specific event exists and count by date
SELECT event_date, COUNT(*) AS event_count
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
  AND event_name = '{EVENT_NAME}'
GROUP BY event_date
ORDER BY event_date
```

## Validate Consent Mode

```sql
-- Check consent signals in events
SELECT
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'gcs') AS consent_state,
  COUNT(*) AS event_count
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
GROUP BY consent_state
ORDER BY event_count DESC
```

## Client vs Server Comparison

```sql
-- Compare event counts by platform (web = client, server = sGTM)
SELECT
  platform,
  event_name,
  COUNT(*) AS cnt
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
GROUP BY platform, event_name
ORDER BY event_name, platform
```

## User Journey

```sql
-- Page path sequence for a specific user
SELECT
  event_timestamp,
  event_name,
  (SELECT value.string_value FROM UNNEST(event_params) WHERE key = 'page_location') AS page,
  (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS session_id
FROM `zipmend-2e643.analytics_287815421.events_*`
WHERE _TABLE_SUFFIX BETWEEN '{START_DATE}' AND '{END_DATE}'
  AND user_pseudo_id = '{USER_PSEUDO_ID}'
ORDER BY event_timestamp
```
