# Data Validation Report: {tag_or_event_name}

**Date**: {date}
**Container**: {container_name}
**Validator**: Claude Code

## Tag Configuration

| Field | Value |
|---|---|
| Tag Name | {tag_name} |
| Tag Type | {tag_type} |
| Event Name | {event_name} |
| Firing Trigger | {trigger_name} |
| Consent Required | {consent_type} |

## Validation Results

### Data Presence
| Check | BQ (GA4) | Firestore | Status |
|---|---|---|---|
| Event exists | {bq_event_count} events | {fs_event_count} events | {status} |
| Date range | {bq_date_range} | {fs_date_range} | {status} |
| User IDs present | {bq_user_pct}% | {fs_user_pct}% | {status} |

### Parameter Completeness
| Parameter | Expected | BQ Present | FS Present | Status |
|---|---|---|---|---|
| {param_name} | {expected} | {bq_present} | {fs_present} | {status} |

### Ecommerce Data (if applicable)
| Field | Expected | BQ | FS | Status |
|---|---|---|---|---|
| transaction_id | Present | {bq} | {fs} | {status} |
| value | > 0 | {bq} | {fs} | {status} |
| currency | EUR | {bq} | {fs} | {status} |
| items | Non-empty | {bq} | {fs} | {status} |

### Consent Compliance
| Check | Result | Status |
|---|---|---|
| Consent signals present | {result} | {status} |
| Events respect consent | {result} | {status} |

## Discrepancies Found
{discrepancies}

## Recommendations
1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}

## Queries Used
```sql
-- BQ validation query
{bq_query}
```

```bash
-- Firestore validation command
{fs_command}
```
