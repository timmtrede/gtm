---
name: Test sGTM against actual Firestore data, not BQ snapshots
description: When sGTM reads from Firestore at runtime, test expected values must use current Firestore data — BQ training snapshots may have diverged
type: feedback
---

For sGTM templates that read from Firestore, test expected values must be computed using the ACTUAL current Firestore document, not a BQ snapshot of the same data.

**Why:** During DATA-375, the `ml.company_scoring_data_v4` BQ table had different NACE codes and feature values than the live Firestore `scores` documents for the same domains. BQ had `k=1, n=1` while Firestore had `nace_codes: ["70.2","62.2","62.9"]` (→ `j=1, m=1`). This caused expected probabilities to be wildly off.

**How to apply:**
1. For each test domain, fetch the actual Firestore document
2. Use Firestore fields for domain-level features (company profile, NACE)
3. Use the test payload for event-level features (revenue, vehicle, payment, etc.)
4. Compute expected values from this combined input
