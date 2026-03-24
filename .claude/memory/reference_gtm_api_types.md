---
name: GTM API variable type codes for server containers
description: Correct type strings for creating GTM variables via the API — discovered through trial and error
type: reference
---

Server container variable types for the GTM API v2:

| Variable type | API `type` value | Key parameter |
|---|---|---|
| Event Data | `ed` | `keyPath` (template) |
| Data Layer (web) | `v` | `name` (template) |
| Constant | `c` | `value` (template) |
| Lookup Table | `smm` | `input`, `map` |
| Regex Lookup | `remm` | `input`, `map` |
| Server Cookie | `sgtmk` | `name` |
| Request Header | `rh` | `headerName` |
| Custom Template | `cvt_{containerId}_{templateId}` | per template |

Common mistake: `sgtmed` is NOT a valid type — use `ed` with `keyPath` parameter.

Parameter type values are lowercase in server containers: `"template"`, `"boolean"` (not `"TEMPLATE"`, `"BOOLEAN"`).

Advanced Lookup Table template ID in Zipmend server container: `cvt_171542205_22`.
Firestore Writer template ID: `cvt_171542205_112`.
