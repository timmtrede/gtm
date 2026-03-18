# BigQuery Cost Guide

## Pricing Model (On-Demand)
- **Queries**: $6.25 per TB scanned (first 1 TB/month free)
- **Storage**: $0.02/GB/month (active), $0.01/GB/month (long-term >90 days)

## Zipmend Cost Context
- GA4 daily table: ~1.5-2.5 MB per day (~42k events)
- GA4 monthly: ~50-75 MB
- Full year scan: ~600-900 MB
- `SELECT *` on all GA4 tables: ~9 GB (~$0.06)
- Most targeted queries: <100 MB (effectively free)

## Safety Guards

### maximum_bytes_billed
Already configured in the project at 10 GB:
```python
job_config = bigquery.QueryJobConfig(
    maximum_bytes_billed=10 * 1024 * 1024 * 1024,  # 10 GB
)
```
Query fails before executing if it would exceed this limit.

### Dry Run
Always estimate cost before running expensive queries:
```bash
gtm bq query --dry-run "SELECT ..."
```

## Cost Optimization Tips

### 1. Limit table scans with _TABLE_SUFFIX
```sql
-- Bad: scans ALL daily tables
SELECT * FROM `analytics_287815421.events_*`

-- Good: scans one day only
SELECT * FROM `analytics_287815421.events_*`
WHERE _TABLE_SUFFIX = '20250301'

-- Good: scans one month
WHERE _TABLE_SUFFIX BETWEEN '20250301' AND '20250331'
```

### 2. Select only needed columns
```sql
-- Bad: reads all columns (~2 MB per day)
SELECT * FROM events_20250301

-- Good: reads only event_name column (~50 KB per day)
SELECT event_name FROM events_20250301
```

### 3. Use processed tables when possible
`superform_outputs_287815421` has pre-aggregated tables:
- `ga4_sessions` — session-level data (much smaller than raw events)
- `ga4_transactions` — transaction-level data
- `ga4_events` — cleaned event data

### 4. Use preview instead of query
```bash
# Zero cost — uses list_rows API, not a query
gtm bq preview analytics_287815421 events_20250301 --limit 10
```

### 5. Cache-friendly queries
BigQuery caches identical queries for 24 hours. Same query = zero cost on repeat.

## Cost Estimation Cheat Sheet
| Query Type | Estimated Bytes | Cost |
|---|---|---|
| One day, all columns | ~2 MB | Free |
| One month, all columns | ~75 MB | Free |
| One year, all columns | ~900 MB | Free |
| All time, all columns | ~9 GB | ~$0.06 |
| One day, one column | ~50 KB | Free |
| DWH tables (varies) | 1-500 MB | Free to ~$0.003 |
