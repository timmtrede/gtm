---
name: Always analyze GTM container conventions before implementing
description: Do a full naming convention audit of both web and server containers before creating new resources
type: feedback
---

Before creating any GTM resources, run a comprehensive analysis of all existing variables, tags, and triggers in both containers to understand naming patterns and structural conventions.

**Why:** During DATA-375 we initially created variables without checking conventions, then discovered the container has strict dot-separated naming (`ed.*`, `tr.*`, `alookup.*`, `firestore.*`, `c.*`, `scoring.*`), specific type-to-prefix mappings, and patterns like `not.*`/`only.*`/`event.*` for triggers. This also revealed that the `alookup.gads_variable_label` outputs actual Google Ads conversion label IDs, not descriptive names — a critical detail missed in the initial spec.

**How to apply:** Before any GTM implementation:
1. List all resources grouped by naming prefix
2. Document the prefix → GTM type mapping
3. Check existing resources that will be modified (get full raw API config)
4. Verify assumptions about how existing variables behave (types, null handling, etc.)
