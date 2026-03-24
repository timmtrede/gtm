---
name: BigQuery is the source of truth for model validation
description: When testing ML model implementations, BQ training data defines expected behavior — adapt the implementation to match BQ, not the other way around
type: feedback
---

When validating an ML model implementation (e.g., in sGTM), the BigQuery training data table is the source of truth for expected values.

**Why:** During DATA-375 testing, we initially adapted the test expected values to match what sGTM produced (wrong). The user corrected this — the BQ `ml.company_scoring_data_v4` table defines what the model SHOULD produce. If sGTM disagrees, the bug is in sGTM.

**How to apply:**
1. Compute expected values from BQ training data features
2. Build test payloads that reproduce BQ feature values in the sGTM pipeline
3. If sGTM output differs, debug the sGTM implementation — don't adjust expected values
4. Only document known mapping gaps (like `online=null` in BQ vs always-present `order_origin` in production) as explicit discrepancies, not as adjustments to expectations
