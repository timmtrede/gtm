---
name: DATA-375 scoring model v4 deployment complete
description: ML-based conversion value scoring for Google Ads — deployed to production across 3 phases
type: project
---

**Completed:** 2026-03-24
**JIRA:** DATA-375
**Spec:** `specs/gads-scoring-value.md`
**Test cases:** `specs/test-cases-scoring.md` (18 cases)

## What was built

Logistic regression model (`company_scoring_v4`) running in sGTM to score non-generic first-order purchases. Adjusts the conversion value sent to Google Ads based on predicted probability of 3+ orders.

**Formula:** `multiplier = clamp(probability * 3, 0.6, 2.4); adjusted_value = multiplier * revenue`

**Label buckets:** B-Kunden (<0.8), A-Kunden ([0.8,1.2]), A+ Kunden (>1.2)

## GTM resources created/modified

- 3 custom templates + variables: `scoring.conversion_probability`, `scoring.adjusted_value`, `scoring.label`
- `ed.value_eur` (server) + `dlv.value_eur` (web) + `ga4.purchase` tag updated
- `alookup.gads_variable_value` and `alookup.gads_variable_label` updated
- `firestore.write.scores.conversion_probability` tag writes probability back to Firestore
- Deleted: `tr.value.70%`, `firestore.scores.purchase`

## Key files

- `src/gtm/templates/scoring_model_v4.js` — testable JS model with all weights
- `src/gtm/templates/sgtm_scoring_conversion_probability.tpl` — sGTM template code (with debug logs)
- `src/gtm/templates/sgtm_scoring_adjusted_value.tpl` / `sgtm_scoring_label.tpl`
- `src/gtm/templates/test_scoring_model_v4.js` — 86 unit tests
- `src/gtm/templates/generate_test_cases.js` — generates test payloads from BQ+Firestore data
- `src/gtm/templates/deploy_scoring.py` — API deployment script

## Known discrepancies

- BQ `online=null` maps to sGTM `online="false"` in production (front-end always sends `order_origin`)
- Firestore scoring data may differ from BQ training snapshot for some domains
- Sigmoid uses (1+x/65536)^65536 approximation (~6 decimal places, not exact Math.exp)

**How to apply:** This is the reference for any future model updates (v5+). Extract new weights from BQ, update the JS file and sGTM template, regenerate test cases.
