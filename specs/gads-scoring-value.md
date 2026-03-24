# Spec: ML-Based Conversion Value Scoring for Google Ads

**Status:** Ready for Implementation
**JIRA:** [DATA-375](https://zipmend.atlassian.net/browse/DATA-375)
**Author:** Jeremie Er-Rafiqi
**Date:** 2026-03-19
**GTM Workspace:** `DATA-375 New scoring logic for Gads Transaction Values`

---

## Overview

Add a scoring-based value adjustment for **non-generic first-order purchases** sent to Google Ads via the server-side GTM container (`GTM-5X8VX8N7`). The model (`company_scoring_v4`) is a logistic regression that predicts the probability of a domain placing 3+ orders, and uses that probability to scale the reported conversion value.

### Scope

The new scoring logic applies **only** when ALL conditions are met:

1. The purchase is a **first order** (user_id not found in Firestore `existing_customers` — same logic as trigger `event.purchase.first_order`, ID 187)
2. The buyer's email domain is **not a generic domain** (not in Firestore `generic_domains`)
3. The buyer's domain **has a scoring document** in Firestore `scores`

**All other cases use simplified existing logic. In case of any error, always fall back to `ed.value` (100% unmodified).**

Note: uppercase/lowercase does not matter for feature values.

### Simplified Value Routing (replaces current is_b logic)

| Condition | Value sent to Google Ads |
|-----------|------------------------|
| Generic email domain | `ed.value * 0.5` |
| Non-generic, first order, has score | `scoring.adjusted_value` (new) |
| Non-generic, non-first order | `ed.value` (unmodified) |
| Default / error | `ed.value` (unmodified) |

The `is_b` flag and ~70% logic are **removed**. Assets `tr.value.70%` (ID 270), `firestore.scores.purchase` (ID 250) can be scrapped.

### Value Formula (for scored non-generic first orders)

```
multiplier = probability * 3
if multiplier > 2.4: multiplier = 2.4   # cap
if multiplier < 0.6: multiplier = 0.6   # floor
adjusted_value = multiplier * revenue
```

Examples (revenue = EUR1000):
- prob=0.50 → 0.5x3 = 1.5 → 1.5 x 1000 → **EUR1500**
- prob=0.10 → 0.1x3 = 0.3 < floor(0.6) → 0.6 x 1000 → **EUR600**
- prob=0.90 → 0.9x3 = 2.7 > cap(2.4) → 2.4 x 1000 → **EUR2400**

---

## Requirements

### R1: sGTM Custom Variable Template — Conversion Probability

Create a custom variable template `scoring.conversion_probability` that (naming note: this introduces a new `scoring.*` prefix for ML-derived variables, complementing the existing `tr.*` prefix for simple transformations and `firestore.*` for lookups):

- Gathers features from Firestore `scores` collection + purchase event data
- Implements `predictConversionProbability()` from model `company_scoring_v4`
- Returns the conversion probability (0–1), clamped by sigmoid
- Returns `null` on any error or when conditions are not met (triggers fallback downstream)

### R2: sGTM Custom Variable — Adjusted Value

Create a variable `scoring.adjusted_value` that:

- Reads `scoring.conversion_probability` and `ed.value`
- Computes: `multiplier = clamp(prob * 3, 0.6, 2.4); result = multiplier * value`
- Returns `null` if probability is `null` (falls through to existing logic)
- Rounds to 2 decimal places

### R3: Update the Value Routing Logic

Update `alookup.gads_variable_value` (variable 177) to implement the new simplified logic:

| Priority | Condition | Value |
|----------|-----------|-------|
| 1 | Generic domain (`firestore.generic_domains.purchase` != "false") | `tr.value.50%` |
| 2 | Non-generic first order with score → `scoring.adjusted_value` is not null | `scoring.adjusted_value` |
| 3 | Default (non-generic non-first order, or scoring returned null) | `ed.value` |

**Removed:** The `is_b` / `firestore.scores.purchase` check and the ~70% rule.
**Removed assets:** `tr.value.70%` (ID 270), `firestore.scores.purchase` (ID 250) — can be deleted.
**Kept:** `tr.value.50%` (ID 233) for generic domains.

### R4: Update Customer Groups Label Logic

Update `alookup.gads_variable_label` (ID 258) to segment conversions for monitoring via `gads.purchase.customer_groups` (tag 257). Labels are actual Google Ads conversion label IDs.

| Condition | Multiplier (`prob*3`, clamped) | Segment | Google Ads label |
|-----------|-------------------------------|---------|------------------|
| Generic domain | — | Generic | `E8KBCLuyveYaEObk9sED` |
| Non-generic, non-first order | — | Bestandskunden | `im7ACJLI2YscEObk9sED` |
| Non-generic, first order | < 0.8 | B-Kunden | `kIETCImEtuYaEObk9sED` |
| Non-generic, first order | [0.8, 1.2] | A-Kunden | `5PHlCJX_qOYaEObk9sED` |
| Non-generic, first order | > 1.2 | A+ Kunden | `2JWlCIOsqIwcEObk9sED` |

**Implementation:** The `scoring.conversion_probability` template returns the probability. A companion variable `scoring.label` computes the multiplier (`prob * 3`, clamped to [0.6, 2.4]) and returns the appropriate label string (`"b_kunden"`, `"a_kunden"`, `"a_plus_kunden"`). The `alookup.gads_variable_label` maps these strings + generic/non-first conditions to the Google Ads labels above.

### R5: Feature Input Mapping

The v4 model requires these features:

| Feature | Source | Mapping Notes |
|---------|--------|---------------|
| **Company profile** (12 features) | Firestore `scores` | `no_shipping_required`, `b2b_business_model`, `logistics_transportation`, `min_200_employees`, `non_eu_operations`, `turnover_10m_to_500m_eur`, `heavy_large_products`, `operates_europe_wide`, `manufactures_product`, `mainly_b2c`, `high_quality_physical_goods`, `low_cost_consumer_products` — STRING "true"/"false"/"unknown" |
| **NACE one-hot** (`a`–`u`, 21 flags) | Firestore `scores` → `nace_code` | JSON array of codes, e.g. `["49.4","50.2","52.2"]`. Parse array, map each code's integer prefix to its NACE section letter. **Multiple letters can be 1** for a single domain. See [NACE Mapping](#nace-mapping). |
| `net_revenue_first_transport` | Purchase event | `value_eur`. **Requires new variable setup** — exists in dataLayer but NOT sent by ga4.purchase tag. See [value_eur Setup](#value_eur-setup). |
| `distance_first_transport` | Purchase event items | `items[0].distance` (int). In sGTM, read from items array or use existing `tr.t_details.distance` (parsed from `t_details` composite string). |
| `transport_type_first_transport` | Purchase event items | `item_category` from items array: `"express"` → `"express_1200_kg"`, `"lkw"` → `"full_truck_24_t"`. |
| `vehicle_type_first_transport` | Purchase event items | `item_id` (STRING, e.g. `"11"`) from items where `item_list_name` contains `"main_products"`. Map via `dm_stg.stg_mapping_vehicle_type_labels`. See [Vehicle Type Mapping](#vehicle-type-mapping). |
| `online` | Purchase event | `order_origin` param: `"true"` if order_origin == `"online"`, else `"false"`. |
| `payment_method` | Purchase event | Event param `payment_type`. Direct match for most values. `sofort` → map to `klarna` (same provider). `trustly` → deprecated (0 orders since Mar 2025), ignore. See [Payment Method Mapping](#payment-method-mapping). |
| `shipper_language` | Purchase event | **NOT sent from web container.** `cjs.language_code` exists (parses `/v2/{lang}/` from URL) but only used by Facebook tags. **Requires setup** — either add to ga4.purchase tag or parse from `page_path` in sGTM. See [language_code Setup](#language_code-setup). |
| `loading_country_code` | Purchase event items | First 2 chars of `items[0].loading_location` (format: `CC_PostalCode_City`, e.g. `DE_22041_Hamburg`). In dataLayer it's inside items, not event-level. |
| `unloading_country_code` | Purchase event items | First 2 chars of `items[0].unloading_location`. Same as above. |
| `tld` | Derived from domain | Extract TLD from domain string (e.g., `"example.de"` → `".de"`). |

**Dropped from v2 → v4:** `score`, `weight_first_transport`, `hours_til_transport`, `shipper_country_code`, `industry_fit`

---

## Data Investigations

### NACE Mapping

Source: `zipmend-2e643.dm_mapping.nace_classification_mapping` — maps NACE Rev 2.1 numeric codes to 22 section letters (A–V).

**Mapping logic for the sGTM template:**

1. Read `nace_code` from Firestore `scores` document — it's a JSON string array, e.g. `["49.4","50.2","52.2"]`
2. Parse the array
3. For each code, take the integer part before the decimal (e.g., `"49.4"` → `49`)
4. Map the integer division code to its NACE section letter using the standard division ranges:

| Division codes | Section | Model column |
|---|---|---|
| 01–03 | A | `a` |
| 05–09 | B | `b` |
| 10–33 | C | `c` |
| 35 | D | `d` |
| 36–39 | E | `e` |
| 41–43 | F | `f` |
| 45–47 | G | `g` |
| 49–53 | H | `h` |
| 55–56 | I | `i` |
| 58–63 | J | `j` |
| 64–66 | K | `k` |
| 68 | L | `l` |
| 69–75 | M | `m` |
| 77–82 | N | `n` |
| 84 | O | `o` |
| 85 | P | `p` |
| 86–88 | Q | `q` |
| 90–93 | R | `r` |
| 94–96 | S | `s` |
| 97–98 | T | `t` |
| 99 | U | `u` |

5. Set each matched lowercase letter column to 1 (multiple can be 1 if domain has codes spanning multiple sections)
6. All unmatched columns remain 0
7. If no `nace_code` or empty array, all columns stay 0

### Payment Method Mapping

GA4 event param is `payment_type`. Model trained on DWH `payment_method`.

| GA4 `payment_type` | Model weight key | Notes |
|----|----|----|
| `creditcard` | `creditcard` | Direct |
| `invoice` | `invoice` | Direct |
| `paypal` | `paypal` | Direct |
| `klarna` | `klarna` | Direct |
| `bancontact` | `bancontact` | Direct |
| `ideal` | `ideal` | Direct |
| `przelewy24` | `przelewy24` | Direct |
| `belfius` | `belfius` | Direct |
| `billie` | `billie` | Direct |
| `advancePayment` | `advancePayment` | Direct. DWH `advance_payment` and `advance_payment_wise` also map here. |
| (any unknown) | — | Weight 0 (unknown category baseline) |

**Mappings:**
- DWH `sofort` → map to `klarna` (same provider, Sofort was acquired by Klarna)
- DWH `trustly` → deprecated, 0 orders since March 2025. Ignore (weight 0 if encountered).
- DWH `advance_payment` / `advance_payment_wise` → GA4 sends `advancePayment` (direct match to model key)

### Vehicle Type Mapping

GA4 `item_name` values are **localized** (75 values across 8+ languages). The model uses English labels. Use `item_id` (numeric, stable across languages) mapped via `zipmend-2e643.dm_stg.stg_mapping_vehicle_type_labels`.

**Full mapping** (from `stg_mapping_vehicle_type_labels`):

| item_id | Label (= `vehicle_type_number` → `vehicle_type_label`) | Model weight key |
|---------|-------------------------------------------------------|-----------------|
| 0 | Large van | `Large van` |
| 1 | Tail lift and pallet truck | `Tail lift and pallet truck` |
| 2 | Length 450cm loading space | `Length 450cm loading space` |
| 3 | Length 480cm loading space | `Length 480cm loading space` |
| 4 | Width 220cm loading space | `Width 220cm loading space` |
| 5 | Width 230cm loading space | `Width 230cm loading space` |
| 6 | Ramp height | — (not in model, use `_null`) |
| 7 | Overhang | `Large van` (mapped to big van) |
| 8 | Loading from above | `Loading from above` |
| 9 | Dangerous Goods | `Dangerous Goods` |
| 10 | Cooling-vehicle | `Large van` (mapped to big van) |
| 11 | Small van | `Small van` |
| 12 | Medium van | `Medium van` |
| 13 | 24t Shipment | `24t Shipment` |
| 14 | 2,4t Shipment | `2,4t Shipment` |
| 15 | 5t Shipment | `5t Shipment` |
| 16 | 12t Shipment | `12t Shipment` |
| 17 | 3,2t Shipment | `3,2t Shipment` |
| 18 | 1t Shipment | — (not in model, use `_null`) |

**Implementation:**
- Filter items where `item_list_name` contains `"main_products"`
- Take the first matching item's `item_id`
- Look up the model weight key from the hardcoded map above
- Items from `_extras` lists are secondary features, not the primary vehicle
- Missing model keys (item_id 6, 18): use `_null` weight
- Overhang (7) and Cooling-vehicle (10): map to `Large van` (big van equivalent)

### value_eur Setup

The model feature `net_revenue_first_transport` requires the value in EUR. `value_eur` exists in the dataLayer but is **NOT sent** by the `ga4.purchase` tag (ID 470) — only `value` is sent.

**Required setup:**
1. **Web container (32433317)**: Create a data layer variable `dlv.value_eur` reading `dataLayer.value_eur`
2. **Web container**: Add `value_eur` as an event parameter in the `ga4.purchase` tag (ID 470)
3. **Server container (171542205)**: Create an event data variable `ed.value_eur` reading event data key `value_eur`

The scoring template will use `ed.value_eur` for `net_revenue_first_transport`. If `value_eur` is not available (null), fall back to `ed.value`.

### language_code Setup

The model feature `shipper_language` requires a language code (e.g., `"de"`, `"en"`). The web container has `cjs.language_code` (parses from URL path `/v2/{lang}/...`) but it is **only used by Facebook tags** — NOT sent as a GA4 event parameter.

**Options:**
1. **Add to ga4.purchase tag**: Add `language_code` = `{{cjs.language_code}}` as an event parameter in tag 470. Then create `ed.language_code` in the server container.
2. **Parse from `page_path` in sGTM**: The `page_path` event param is already sent (e.g., `/v2/de/booking/...`). Extract the segment after `/v2/` in the sGTM template. No web container changes needed.

**Recommendation:** Option 2 — parse from `page_path` in the sGTM template. Avoids touching the web container for this. The regex is simple: extract the 2-char segment after `/v2/`.

---

## Architecture

### Option B: Two Separate Variables (confirmed)

**Variable 1: `scoring.conversion_probability`** (custom variable template)
1. Check conditions:
   - `lookup.first_order` == "true" (reuse existing variable ID 201)
   - `firestore.generic_domains.purchase` == "false" (reuse existing variable ID 255)
   - Domain has a document in Firestore `scores`
2. If conditions not met → return `null`
3. Fetch scoring features from Firestore `scores` (company profile + nace_code)
4. Gather event-level features: `ed.value_eur` (fallback `ed.value`), `payment_type`, `order_origin`, `page_path`
5. Extract from items array (first item where `item_list_name` contains "main_products"):
   - `item_id` → vehicle_type mapping (STRING, e.g. "11" → "Small van")
   - `item_category` → transport_type mapping ("express" → "express_1200_kg", "lkw" → "full_truck_24_t")
   - `distance` → distance_first_transport
   - `loading_location` → first 2 chars = loading_country_code
   - `unloading_location` → first 2 chars = unloading_country_code
6. Parse `shipper_language` from `page_path` (`/v2/{lang}/...`)
7. Extract `tld` from domain
7. Map NACE codes to one-hot columns
8. Run logistic regression with v4 weights
9. Return probability (0–1) or `null` on error

**Variable 2: `scoring.adjusted_value`** (simple variable)
1. Read `scoring.conversion_probability`
2. If `null` → return `null`
3. Compute `multiplier = clamp(prob * 3, 0.6, 2.4)`
4. Return `multiplier * ed.value`

**Variable 3: `scoring.label`** (simple variable)
1. Read `scoring.conversion_probability`
2. If `null` → return `null`
3. Compute `multiplier = clamp(prob * 3, 0.6, 2.4)`
4. If multiplier < 0.8 → return `"b_kunden"`
5. If multiplier <= 1.2 → return `"a_kunden"`
6. Else → return `"a_plus_kunden"`

### Integration

**`alookup.gads_variable_value`** (variable 177) — updated routing:

| Rule | Condition | Output |
|------|-----------|--------|
| 1 | `firestore.generic_domains.purchase` != "false" | `tr.value.50%` |
| 2 | `scoring.adjusted_value` is not null | `scoring.adjusted_value` |
| 3 | Default | `ed.value` |

**`alookup.gads_variable_label`** (ID 258) — updated routing:

| Rule | Condition | Output (Google Ads label) |
|------|-----------|--------------------------|
| 1 | `firestore.generic_domains.purchase` != "false" | `E8KBCLuyveYaEObk9sED` (Generic) |
| 2 | `scoring.label` == "b_kunden" | `kIETCImEtuYaEObk9sED` (B-Kunden) |
| 3 | `scoring.label` == "a_kunden" | `5PHlCJX_qOYaEObk9sED` (A-Kunden) |
| 4 | `scoring.label` == "a_plus_kunden" | `2JWlCIOsqIwcEObk9sED` (A+ Kunden) |
| 5 | Default (non-first order or scoring returned null) | `im7ACJLI2YscEObk9sED` (Bestandskunden) |

### sGTM Template Considerations

- sGTM sandboxed JS: `Math.exp()` may not be available — implement sigmoid as `1 / (1 + exp(-z))` using available math utilities or a manual implementation
- Firestore reads use existing `Firestore.read()` pattern
- Model weights are hardcoded constants — no external API
- Items array access: need to verify sGTM API for reading items from the event data
- **Future model updates:** Weights extractable via `ML.WEIGHTS(MODEL ...)` if model is trained as BQML logistic regression

### Affected GTM Resources

| Resource | Container | ID | Change |
|----------|-----------|-----|--------|
| **Web container changes** | | | |
| New: `dlv.value_eur` | Web (32433317) | — | New data layer variable reading `dataLayer.value_eur` |
| `ga4.purchase` tag | Web (32433317) | 470 | Add `value_eur` as event parameter |
| **Server container changes** | | | |
| New: `scoring.conversion_probability` | Server (171542205) | — | New custom variable template (model + feature gathering) |
| New: `scoring.adjusted_value` | Server | — | New variable (value formula: clamp(prob*3, 0.6, 2.4) * value) |
| New: `scoring.label` | Server | — | New variable (label bucketing: b_kunden/a_kunden/a_plus_kunden) |
| New: `ed.value_eur` | Server | — | New event data variable reading `value_eur` |
| `alookup.gads_variable_value` | Server | 177 | Simplified routing (remove is_b, add scoring rule) |
| `alookup.gads_variable_label` | Server | — | Updated label bucketing for monitoring |
| `tr.value.70%` | Server | 270 | **Delete** (is_b logic removed) |
| `firestore.scores.purchase` | Server | 250 | **Delete** (is_b logic removed) |
| `gads.purchase.online` | Server | tag 90 | **No change** |
| `gads.purchase.online.vehicle_category` | Server | tag 21 | **No change** |
| `gads.purchase.online.first_order` | Server | tag 179 | **No change** |
| `gads.purchase.customer_groups` | Server | tag 257 | **No change** (label variable updated) |
| `tr.value.50%` | Server | 233 | **Kept** |

Note: `shipper_language` is parsed from `page_path` (`/v2/{lang}/...`) in the sGTM template — no additional GTM variables needed.

### All changes in workspace: `DATA-375 New scoring logic for Gads Transaction Values`

**DO NOT publish.** Jeremie will publish manually.

---

## First-Order Detection Logic (reference)

From trigger `event.purchase.first_order` (ID 187) and variable `lookup.first_order` (ID 201):

```
Purchase event → ed.user_id
  → Firestore query: existing_customers WHERE user_id == ed.user_id
    → Document found → NOT first order (lookup.first_order = "false")
    → No document   → FIRST ORDER (lookup.first_order = "true")
```

Reuse `lookup.first_order` to gate the scoring model.

---

## Implementation Plan

### Phase 1: Setup value_eur Pipeline
1. Create `dlv.value_eur` variable in web container (32433317)
2. Add `value_eur` event parameter to `ga4.purchase` tag (ID 470) in web container
3. Create `ed.value_eur` event data variable in server container (171542205)
4. Test: verify `value_eur` flows from dataLayer → GA4 request → server container event data

### Phase 2: Build the Templates
1. Create `scoring.conversion_probability` custom variable template:
   - v4 model weights (intercept + numeric + categorical)
   - Feature gathering (Firestore scores + event data + items)
   - NACE mapping, vehicle_type mapping, payment mapping, country code extraction
   - Gating: first order + non-generic + has score
   - Error handling: return `null` on any failure
2. Create `scoring.adjusted_value` variable
3. Unit test JS function locally against DATA-375 example

### Phase 3: Deploy to GTM Workspace
1. Create both scoring variables in the `DATA-375` workspace
2. Update `alookup.gads_variable_value` (simplified routing)
3. Update `alookup.gads_variable_label` (probability bucketing)
4. Delete `tr.value.70%` (ID 270) and `firestore.scores.purchase` (ID 250)

### Phase 4: Validation (manual, by Jeremie)
1. GTM preview mode: verify values on test transactions
2. Compare sample of domains: old value vs new value
3. Verify customer groups labels show correct buckets
4. Publish when satisfied

---

## Testing Plan

- [ ] Unit test: JS sigmoid function produces correct probability for the DATA-375 example
- [ ] Unit test: Value formula edge cases (prob=0, prob=0.29, prob=0.30, prob=0.5, prob=0.75, prob=0.99)
- [ ] Unit test: NACE code parsing from JSON array `["49.4","50.2"]` → sections H, H (both map to H, so `h`=1)
- [ ] Unit test: NACE code spanning multiple sections `["25.1","49.4"]` → `c`=1, `h`=1
- [ ] Unit test: Vehicle type mapping (item_id 0 → "Large van", item_id 12 → "Medium van", item_id 17 → "3,2t Shipment")
- [ ] Unit test: Country code extraction ("DE_68199_Mannheim" → "DE")
- [ ] Unit test: Model returns `null` for generic domains, non-first orders, missing scores
- [ ] Unit test: Label bucketing (prob=0.2 → b_kunden, prob=0.35 → a_kunden, prob=0.5 → a_plus_kunden)
- [ ] Unit test: Fallback to `ed.value` on any error
- [ ] Validation: Compare model output for sample domains against known BQ predictions
- [ ] GTM Preview: End-to-end test with a real purchase event (manual)

---

## Open Questions

No open questions remaining. All resolved — see below.

---

## Resolved Questions

| # | Question | Resolution |
|---|----------|------------|
| 1 | Where do first-transport features come from? | From purchase event data. v4 dropped `weight_first_transport` and `hours_til_transport`. |
| 2 | Are payment/geo features in the event? | Yes. `payment_type`, `language_code`, `loading_location`, `unloading_location`, `distance`, `order_origin` all present. |
| 3 | Fallback for unknown domains? | Fall back to `ed.value` (no alteration). Model only for non-generic first orders with score. |
| 4 | What is `online`? | Derived from `order_origin`: "true" if online, "false" if offline. |
| 5 | Generic domain pre-filter? | Yes, model does NOT apply. Generic → 50% (existing logic). |
| 6 | Architecture? | Option B: two separate variables. |
| 7 | NACE columns? | Not in Firestore directly. Parse `nace_code` JSON array from scores doc, map to section letters. Multiple letters can be 1. |
| 8 | Keep old variables? | `tr.value.50%` kept. `tr.value.70%` and `firestore.scores.purchase` deleted (is_b logic removed). |
| 9 | is_b logic? | Removed entirely. Non-generic non-first orders get `ed.value` (100%). |
| 10 | Payment mapping? | `advance_payment` + `advance_payment_wise` → `advancePayment`. `sofort`/`trustly` ignored. |
| 11 | Vehicle type source? | `item_name` where `item_list_name` contains "main_products". Use `item_id` for stable cross-language mapping. |
| 12 | Transport type? | `item_category`: "express" → "express_1200_kg", "lkw" → "full_truck_24_t". |
| 13 | Language? | `language_code` event param (no page_path parsing needed). |
| 14 | Country codes? | First 2 chars of `loading_location` / `unloading_location`. |
| 15 | Label ranges? | Confirmed: "[1.5 to 2]" for `above_label`. Ranges refer to effective multiplier (prob * 2). |
| 16 | Currency / `value_eur`? | `value_eur` exists in front-end event but needs new variables in client + server containers. Use `ed.value_eur` for model, fallback to `ed.value`. |
| 17 | Multi-item vehicle type? | Use `item_id` from items where `item_list_name` contains "main_products". |
| 18 | Width 220cm, Overhang, Cooling-vehicle? | Overhang (item_id 7) and Cooling-vehicle (item_id 10) → map to `Large van`. Width 220cm (item_id 4) is in the mapping table directly. |
| 19 | Payment: sofort? | Map to `klarna` (same provider). |
| 20 | Payment: trustly? | Deprecated — 0 orders since Mar 2025. Ignore (weight 0). |
| 21 | Vehicle type: localized item_name? | Use `item_id` (numeric, language-independent) mapped via `dm_stg.stg_mapping_vehicle_type_labels`. |
| 22 | `value_eur` in dataLayer? | Confirmed present (`value_eur: 258.13`). NOT sent by ga4.purchase tag — needs to be added. |
| 23 | `distance`, `loading_location`, `unloading_location` location? | In items array, NOT event-level. Server container promotes them via `t_details`/`t_route` parsing. Template should read from items directly. |
| 24 | `language_code` source? | NOT sent from web container. `cjs.language_code` exists but only used by FB tags. Parse from `page_path` in sGTM (`/v2/{lang}/...`). |
| 25 | `item_id` type? | STRING in dataLayer (e.g., `"11"` not `11`). Mapping must use string comparison. |

---


## Future Considerations

- **Model updates:** If trained as BQML, extract weights via `ML.WEIGHTS(MODEL ...)`. Could automate template updates.
- **Vehicle type tracking fix:** GA4 `vehicle_type` event param is broken (always "undefined"/"unknown"). Separate ticket to fix — currently not blocking since we use `item_id` from items array instead.

---

## Implementation Deliverables

### Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `src/gtm/templates/scoring_model_v4.js` | 582 | Core model logic: v4 weights, helpers (NACE mapping, vehicle type mapping, TLD/language/country extraction, boolean conversion), `predictConversionProbability()`, `computeMultiplier()`, `calculateAdjustedValue()`, `getMonitoringLabel()`, `getGadsLabel()`, `buildFeatures()`. Testable standalone in Node.js. |
| `src/gtm/templates/test_scoring_model_v4.js` | 285 | **86 unit tests** (all passing). Covers: DATA-375 JIRA example, multiplier clamping (floor 0.6, cap 2.4, factor 3), value formula (3 JIRA examples), label bucketing (b_kunden/a_kunden/a_plus_kunden), Google Ads label IDs, NACE parsing (single/multi-section, empty), vehicle type mapping (19 item_ids), TLD/language/country extraction, Firestore boolean→string conversion, full feature building from sample data, all-nulls fallback, case insensitivity. |
| `src/gtm/templates/sgtm_scoring_conversion_probability.tpl` | 296 | Complete sGTM sandboxed JS template — ready to paste into GTM UI. Reads domain from `cookie.ed`, gates on `lookup.first_order` + `firestore.generic_domains.purchase`, fetches Firestore `scores` doc, gathers event data + items array, runs logistic regression with v4 weights, returns probability (0–1) or null. |
| `src/gtm/templates/deploy_scoring.py` | 194 | GTM API deployment script. Creates `dlv.value_eur` (web), adds `value_eur` param to `ga4.purchase` tag (web), creates `ed.value_eur` (server). Supports `--dry-run`. |
| `specs/gads-scoring-value.md` | 489 | Complete spec with all requirements, mappings, architecture, resolved questions, implementation deliverables. |

### What the Deployment Script Handles (GTM API)

1. **Web container (32433317):** Create `dlv.value_eur` data layer variable
2. **Web container:** Add `value_eur` event param to `ga4.purchase` tag (ID 470)
3. **Server container (171542205):** Create `ed.value_eur` event data variable

### Manual Steps Remaining (GTM UI)

1. Create `scoring.conversion_probability` custom variable template in server workspace `DATA-375` (ID 46) — paste sandboxed JS from `.tpl` file
2. Create `scoring.adjusted_value` variable — reads probability, applies `clamp(prob * 3, 0.6, 2.4) * ed.value`
3. Create `scoring.label` variable — reads probability, returns `"b_kunden"` / `"a_kunden"` / `"a_plus_kunden"` based on multiplier thresholds
4. Update `alookup.gads_variable_value` (ID 177) — simplified 3-rule routing
5. Update `alookup.gads_variable_label` (ID 258) — 5-rule routing with Google Ads label IDs
6. Delete `tr.value.70%` (ID 270) and `firestore.scores.purchase` (ID 250)

### To Run

```bash
# Tests
node src/gtm/templates/test_scoring_model_v4.js

# Deploy API changes (value_eur pipeline)
.venv/bin/python -m gtm.templates.deploy_scoring --dry-run  # preview
.venv/bin/python -m gtm.templates.deploy_scoring             # deploy
```
