---
name: Production data write protection
description: GOLDEN RULE — Never write to Firestore or BigQuery without double confirmation from the user
type: feedback
---

Never write, update, or delete anything in Firestore or BigQuery without explicit double confirmation from the user.

**Why:** The service account (`claude-gtm-manager`) has write-capable roles (`roles/datastore.user`, `roles/bigquery.jobUser`). These contain production data — Firestore has events, customers, and scores; BigQuery has the full data warehouse (GA4, DWH, reporting, ML). The user declared this a golden rule.

**How to apply:**
- Never add write/update/delete operations to Firestore or BigQuery without asking first
- If a write operation is requested, confirm twice before executing
- All Firestore and BigQuery MCP tools must remain `readOnlyHint: True`
- Default to read-only when building new features for either data store
