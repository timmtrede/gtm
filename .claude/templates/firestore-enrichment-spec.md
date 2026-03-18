# Firestore Enrichment Spec: {title}

**Status**: Draft
**Date**: {date}
**Container**: {container_name} (Server)

## Overview
{description}

## Enrichment Pattern
| Field | Value |
|---|---|
| Pattern | {pattern: lookup / write / stitching / dedup / cogs} |
| Collection | {collection_name} |
| Document Key | {key_field} |
| Trigger Event | {event_name} |
| Template | {template: Firestore Lookup / Artemis / Writer / Custom} |

## Data Flow
```
{event_source} → sGTM → Firestore.{read/write}({collection})
                              ↓
                   Enriched event → {destinations}
```

## Firestore Document Schema
| Field | Type | Description | Example |
|---|---|---|---|
| {field_name} | {type} | {description} | {example} |

## sGTM Configuration

### Variable (Firestore Lookup)
| Setting | Value |
|---|---|
| Collection Path | {collection_path} |
| Query Conditions | {conditions} |
| Key Path | {key_path} |

### Tag (if writing)
| Setting | Value |
|---|---|
| Operation | {add_event_data / merge_keys} |
| Document Path | {doc_path} |
| Data Fields | {fields} |

## Data Population
How the Firestore collection gets its data:
- {source}: {description}
- Refresh frequency: {frequency}
- Volume: {estimated_docs} documents

## Testing Plan
- [ ] Verify collection exists with expected documents
- [ ] Test Firestore Lookup returns correct values
- [ ] Confirm enriched event contains expected fields
- [ ] Check destinations receive enriched data
- [ ] Validate with `gtm firestore query {collection}`
- [ ] Cross-check with `gtm bq query` on GA4 data

## Rollback Plan
{rollback_steps}

## Dependencies
- {dependency_1}
