# DATA-375 — sGTM Scoring Validation Test Cases

Generated: 2026-03-23

## Prerequisites

For each test case:
1. Set cookie `ed` to the test domain (browser devtools or GTM Preview override)
2. Ensure the `user_id` is NOT in Firestore `existing_customers` (the test IDs are unique)
3. Ensure the domain is NOT in Firestore `generic_domains`
4. Ensure the domain IS in Firestore `scores` with matching profile data
5. Open server container GTM Preview, inject the `dataLayer.push()` snippet in the browser console

## Summary

| # | Domain | Probability | Multiplier | Label | Adjusted Value |
|---|--------|-------------|------------|-------|----------------|
| 1 | `baustoff-mill.de` | 0.694645 | 2.0839 | a_plus_kunden | 371.09 |
| 2 | `alaika-advisory.com` | 0.006707 | 0.6000 | b_kunden | 113.74 |
| 3 | `nitec-zerspanung.de` | 0.450898 | 1.3527 | a_plus_kunden | 443.1 |
| 4 | `biscuits-bofin.be` | 0.676454 | 2.0294 | a_plus_kunden | 460.38 |
| 5 | `lewa-system.de` | 0.834078 | 2.4000 | a_plus_kunden | 1444.18 |
| 6 | `bumacogroup.be` | 0.429129 | 1.2874 | a_plus_kunden | 147.66 |
| 7 | `proflextex.de` | 0.755992 | 2.2680 | a_plus_kunden | 1003.31 |
| 8 | `skyline-energy.pl` | 0.015948 | 0.6000 | b_kunden | 959.85 |
| 9 | `happyhorizon.com` | 0.005886 | 0.6000 | b_kunden | 78.18 |
| 10 | `meca-sud.fr` | 0.624476 | 1.8734 | a_plus_kunden | 626.14 |

---

## Case 1: Express, invoice, DE->DE, b2b+manufactures

**Domain:** `baustoff-mill.de`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.694645 |
| multiplier (`prob * 3`, clamped) | 2.0839 |
| `scoring.adjusted_value` | 371.09 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-baustoff-mill.de/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_baustoff-mill.de",
  company_name: "Test baustoff-mill.de",
  company_id: "",
  transaction_id: "TEST-baustoff-mill-de",
  value: 178.07,
  value_eur: 178.07,
  tax: 33.83,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 178.07,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 95,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 2: Express, creditcard, AT->DE, no_shipping_required

**Domain:** `alaika-advisory.com`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.006707 |
| multiplier (`prob * 3`, clamped) | 0.6000 |
| `scoring.adjusted_value` | 113.74 |
| `scoring.label` | `b_kunden` |
| `alookup.gads_variable_label` | `kIETCImEtuYaEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-alaika-advisory.com/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_alaika-advisory.com",
  company_name: "Test alaika-advisory.com",
  company_id: "",
  transaction_id: "TEST-alaika-advisory-com",
  value: 189.57,
  value_eur: 189.57,
  tax: 36.02,
  currency: "EUR",
  payment_type: "creditcard",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 189.57,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "AT_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 125,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 3: Full truck, invoice, DE->DE, NACE c, 3.2t

**Domain:** `nitec-zerspanung.de`

> Note: BQ has `online=null` for this domain. In production, sGTM always receives `order_origin` ("online" or "offline"), so `online` is never null. Expected values below reflect production behavior (`online="false"`).

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.450898 |
| multiplier (`prob * 3`, clamped) | 1.3527 |
| `scoring.adjusted_value` | 443.1 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/full-truck-24-t/test-nitec-zerspanung.de/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_nitec-zerspanung.de",
  company_name: "Test nitec-zerspanung.de",
  company_id: "",
  transaction_id: "TEST-nitec-zerspanung-de",
  value: 327.57,
  value_eur: 327.57,
  tax: 62.24,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "offline",
  items: [
    {
      item_id: "17",
      item_name: "3,2t Shipment",
      price: 327.57,
      quantity: 1,
      item_list_name: "lkw_main_products",
      index: 1,
      item_category: "lkw",
      loading_location: "DE_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 237,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 4: Express, paypal, NL->BE, low_cost_consumer

**Domain:** `biscuits-bofin.be`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.676454 |
| multiplier (`prob * 3`, clamped) | 2.0294 |
| `scoring.adjusted_value` | 460.38 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/nl/booking/express-1200-kg/test-biscuits-bofin.be/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_biscuits-bofin.be",
  company_name: "Test biscuits-bofin.be",
  company_id: "",
  transaction_id: "TEST-biscuits-bofin-be",
  value: 226.86,
  value_eur: 226.86,
  tax: 43.1,
  currency: "EUR",
  payment_type: "paypal",
  order_origin: "online",
  items: [
    {
      item_id: "0",
      item_name: "Large van",
      price: 226.86,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "NL_10115_Test City",
      unloading_location: "BE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 124,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 5: Full truck 24t, invoice, DE->DE, NO profile

**Domain:** `lewa-system.de`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.834078 |
| multiplier (`prob * 3`, clamped) | 2.4000 |
| `scoring.adjusted_value` | 1444.18 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/full-truck-24-t/test-lewa-system.de/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_lewa-system.de",
  company_name: "Test lewa-system.de",
  company_id: "",
  transaction_id: "TEST-lewa-system-de",
  value: 601.74,
  value_eur: 601.74,
  tax: 114.33,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "13",
      item_name: "24t Shipment",
      price: 601.74,
      quantity: 1,
      item_list_name: "lkw_main_products",
      index: 1,
      item_category: "lkw",
      loading_location: "DE_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 170,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 6: Express, bancontact, BE->BE, NACE f

**Domain:** `bumacogroup.be`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.429129 |
| multiplier (`prob * 3`, clamped) | 1.2874 |
| `scoring.adjusted_value` | 147.66 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/nl/booking/express-1200-kg/test-bumacogroup.be/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_bumacogroup.be",
  company_name: "Test bumacogroup.be",
  company_id: "",
  transaction_id: "TEST-bumacogroup-be",
  value: 114.7,
  value_eur: 114.7,
  tax: 21.79,
  currency: "EUR",
  payment_type: "bancontact",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 114.7,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "BE_10115_Test City",
      unloading_location: "BE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 105,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 7: Express, klarna, DE->DE, Large van, NO profile

**Domain:** `proflextex.de`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.755992 |
| multiplier (`prob * 3`, clamped) | 2.2680 |
| `scoring.adjusted_value` | 1003.31 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-proflextex.de/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_proflextex.de",
  company_name: "Test proflextex.de",
  company_id: "",
  transaction_id: "TEST-proflextex-de",
  value: 442.38,
  value_eur: 442.38,
  tax: 84.05,
  currency: "EUR",
  payment_type: "klarna",
  order_origin: "online",
  items: [
    {
      item_id: "0",
      item_name: "Large van",
      price: 442.38,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 344,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 8: Full truck, creditcard, PL->DE, cross-border

**Domain:** `skyline-energy.pl`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.015948 |
| multiplier (`prob * 3`, clamped) | 0.6000 |
| `scoring.adjusted_value` | 959.85 |
| `scoring.label` | `b_kunden` |
| `alookup.gads_variable_label` | `kIETCImEtuYaEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/pl/booking/full-truck-24-t/test-skyline-energy.pl/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_skyline-energy.pl",
  company_name: "Test skyline-energy.pl",
  company_id: "",
  transaction_id: "TEST-skyline-energy-pl",
  value: 1599.75,
  value_eur: 1599.75,
  tax: 303.95,
  currency: "EUR",
  payment_type: "creditcard",
  order_origin: "online",
  items: [
    {
      item_id: "17",
      item_name: "3,2t Shipment",
      price: 1599.75,
      quantity: 1,
      item_list_name: "lkw_main_products",
      index: 1,
      item_category: "lkw",
      loading_location: "PL_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 1200,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 9: Express, ideal, NL->NL, Medium van

**Domain:** `happyhorizon.com`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.005886 |
| multiplier (`prob * 3`, clamped) | 0.6000 |
| `scoring.adjusted_value` | 78.18 |
| `scoring.label` | `b_kunden` |
| `alookup.gads_variable_label` | `kIETCImEtuYaEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/nl/booking/express-1200-kg/test-happyhorizon.com/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_happyhorizon.com",
  company_name: "Test happyhorizon.com",
  company_id: "",
  transaction_id: "TEST-happyhorizon-com",
  value: 130.3,
  value_eur: 130.3,
  tax: 24.76,
  currency: "EUR",
  payment_type: "ideal",
  order_origin: "online",
  items: [
    {
      item_id: "12",
      item_name: "Medium van",
      price: 130.3,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "NL_10115_Test City",
      unloading_location: "NL_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 111,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 10: Express, invoice, FR->FR, Medium van, NO profile

**Domain:** `meca-sud.fr`

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | 0.624476 |
| multiplier (`prob * 3`, clamped) | 1.8734 |
| `scoring.adjusted_value` | 626.14 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/fr/booking/express-1200-kg/test-meca-sud.fr/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_meca-sud.fr",
  company_name: "Test meca-sud.fr",
  company_id: "",
  transaction_id: "TEST-meca-sud-fr",
  value: 334.22,
  value_eur: 334.22,
  tax: 63.5,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "12",
      item_name: "Medium van",
      price: 334.22,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "FR_10115_Test City",
      unloading_location: "FR_20095_Test Destination",
      loading_day: "23-03-2026",
      unloading_day: "23-03-2026",
      distance: 350,
      stopover: "FALSE"
    }
  ]
});
```

---


## Edge Case Tests (Cases 11-15)

These test cases validate the routing logic in `alookup.gads_variable_value` and `alookup.gads_variable_label` for non-scoring scenarios, plus the updated `monitoring.gads.purchase_online.customer_group` tag.

---

## Case 11: Generic domain (gmail.com)

**Cookie `ed`:** `gmail.com`

Scoring should NOT apply. Value = 50% of ed.value, label = Generic.

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | `null` |
| `scoring.adjusted_value` | `null` |
| `scoring.label` | `null` |
| `alookup.gads_variable_value` | 50% of `ed.value` = `125.00` |
| `alookup.gads_variable_label` | `E8KBCLuyveYaEObk9sED` (Generic) |
| `monitoring...customer_group` lead_type | `null-null` or similar |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-gmail/confirmation",
  page_type: "booking_process",
  user_id: "test_edge_generic_gmail",
  company_name: "Test generic",
  company_id: "",
  transaction_id: "TEST-edge-generic",
  value: 250,
  value_eur: 250,
  tax: 47.5,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "0",
      item_name: "Large van",
      price: 250,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Berlin",
      unloading_location: "DE_80331_Munich",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 585,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 12: Non-first order (repeat customer, non-generic domain)

**Cookie `ed`:** `baustoff-mill.de`
**user_id:** Use a user_id that EXISTS in Firestore `existing_customers` (e.g., from a previous test run).

Scoring should NOT apply because it's not a first order. Value = ed.value (100%), label = Bestandskunden.

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | `null` |
| `scoring.adjusted_value` | `null` |
| `scoring.label` | `null` |
| `alookup.gads_variable_value` | `ed.value` = `500.00` (unmodified) |
| `alookup.gads_variable_label` | `im7ACJLI2YscEObk9sED` (Bestandskunden) |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-repeat/confirmation",
  page_type: "booking_process",
  user_id: "test_v3_baustoff-mill.de",
  company_name: "Test repeat customer",
  company_id: "",
  transaction_id: "TEST-edge-repeat",
  value: 500,
  value_eur: 500,
  tax: 95,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 500,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Berlin",
      unloading_location: "DE_80331_Munich",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 585,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 13: Domain not in Firestore scores collection

**Cookie `ed`:** `this-domain-does-not-exist-in-scores.de`

Scoring should NOT apply because no scores document exists. Falls through to default.

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | `null` |
| `scoring.adjusted_value` | `null` |
| `scoring.label` | `null` |
| `alookup.gads_variable_value` | `ed.value` = `300.00` (unmodified) |
| `alookup.gads_variable_label` | `im7ACJLI2YscEObk9sED` (Bestandskunden) |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-noscore/confirmation",
  page_type: "booking_process",
  user_id: "test_edge_noscore_unique",
  company_name: "Test no score",
  company_id: "",
  transaction_id: "TEST-edge-noscore",
  value: 300,
  value_eur: 300,
  tax: 57,
  currency: "EUR",
  payment_type: "creditcard",
  order_origin: "online",
  items: [
    {
      item_id: "0",
      item_name: "Large van",
      price: 300,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Berlin",
      unloading_location: "DE_80331_Munich",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 585,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 14: Scored first order — verify monitoring tag lead_type

**Cookie `ed`:** `baustoff-mill.de` (same as Case 1)

Re-run a scored first order and verify the `monitoring.gads.purchase_online.customer_group` tag writes the correct `lead_type` field to BigQuery.

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | ~0.6946 |
| `scoring.adjusted_value` | ~371.09 |
| `scoring.label` | `a_plus_kunden` |
| `alookup.gads_variable_value` | ~371.09 |
| `alookup.gads_variable_label` | `2JWlCIOsqIwcEObk9sED` (A+ Kunden) |
| Tag 259 `lead_type` field | `a_plus_kunden-0.6946...` (label-probability) |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-baustoff-mill.de/confirmation",
  page_type: "booking_process",
  user_id: "test_v4_baustoff-mill.de",
  company_name: "Test baustoff-mill.de",
  company_id: "",
  transaction_id: "TEST-monitoring-baustoff",
  value: 178.07,
  value_eur: 178.07,
  tax: 33.83,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 178.07,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Test City",
      unloading_location: "DE_20095_Test Destination",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 95,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 15: Non-scored first order — verify `alookup.gads_variable_value` falls through to ed.value

**Cookie `ed`:** `this-domain-does-not-exist-in-scores.de`

Verify that when scoring returns null, `alookup.gads_variable_value` correctly falls through to `ed.value` (not `undefined` or `0`). This tests the `doesNotEqual "undefined"` rule.

### Expected Values

| Variable | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | `null` |
| `scoring.adjusted_value` | `null` (→ fails the "doesNotEqual undefined" check) |
| `alookup.gads_variable_value` | `ed.value` = `750.00` (default, unmodified) |
| `alookup.gads_variable_label` | `im7ACJLI2YscEObk9sED` (Bestandskunden) |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/en/booking/full-truck-24-t/test-fallthrough/confirmation",
  page_type: "booking_process",
  user_id: "test_edge_fallthrough_unique",
  company_name: "Test fallthrough",
  company_id: "",
  transaction_id: "TEST-edge-fallthrough",
  value: 750,
  value_eur: 750,
  tax: 142.5,
  currency: "EUR",
  payment_type: "paypal",
  order_origin: "online",
  items: [
    {
      item_id: "15",
      item_name: "5t Shipment",
      price: 750,
      quantity: 1,
      item_list_name: "lkw_main_products",
      index: 1,
      item_category: "lkw",
      loading_location: "GB_SW1A1AA_London",
      unloading_location: "DE_10115_Berlin",
      loading_day: "24-03-2026",
      unloading_day: "25-03-2026",
      distance: 1100,
      stopover: "FALSE"
    }
  ]
});
```

---

## Phase 3: Firestore Write Tests (Cases 16-18)

These test cases validate that `firestore.write.scores.conversion_probability` (tag 284) writes the `conversion_probability` field to the correct Firestore `scores` document.

**Verification:** After each test, check the Firestore `scores/{domain}` document for a new `conversion_probability` field matching the `scoring.conversion_probability` variable value.

---

## Case 16: Scored first order — verify Firestore write

**Cookie `ed`:** `bumacogroup.be` (Case 6 domain, has scores doc with NACE f)

Scoring applies → tag should fire and write `conversion_probability` to `scores/bumacogroup.be`.

### Expected Values

| Variable / Check | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | ~0.4291 |
| `scoring.label` | `a_plus_kunden` |
| Tag 284 fires? | Yes |
| Firestore `scores/bumacogroup.be` → `conversion_probability` | ~0.4291 |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/nl/booking/express-1200-kg/test-bumacogroup.be/confirmation",
  page_type: "booking_process",
  user_id: "test_phase3_bumacogroup.be",
  company_name: "Test bumacogroup.be",
  company_id: "",
  transaction_id: "TEST-phase3-bumacogroup",
  value: 114.7,
  value_eur: 114.7,
  tax: 21.79,
  currency: "EUR",
  payment_type: "bancontact",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 114.7,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "BE_1000_Brussels",
      unloading_location: "BE_2000_Antwerp",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 105,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 17: Generic domain — verify Firestore write does NOT fire

**Cookie `ed`:** `gmail.com`

Scoring does not apply → tag 284 should NOT fire. No `conversion_probability` field should be written.

### Expected Values

| Variable / Check | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | `null` |
| Tag 284 fires? | **No** (`lookup.first_order` may be "true" but `skipNilValues` prevents the write) |
| Firestore `scores/gmail.com` | No `conversion_probability` field added |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-gmail/confirmation",
  page_type: "booking_process",
  user_id: "test_phase3_gmail",
  company_name: "Test generic",
  company_id: "",
  transaction_id: "TEST-phase3-generic",
  value: 250,
  value_eur: 250,
  tax: 47.5,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "0",
      item_name: "Large van",
      price: 250,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Berlin",
      unloading_location: "DE_80331_Munich",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 585,
      stopover: "FALSE"
    }
  ]
});
```

---

## Case 18: Repeat customer — verify Firestore write does NOT fire

**Cookie `ed`:** `baustoff-mill.de`
**user_id:** Use a user_id that EXISTS in `existing_customers` (e.g., `test_first_order_baustoff-mill.de` from earlier tests).

Not a first order → trigger does not fire → no write.

### Expected Values

| Variable / Check | Expected Value |
|----------|----------------|
| `scoring.conversion_probability` | `null` |
| Tag 284 fires? | **No** (trigger requires `lookup.first_order` == "true") |
| Firestore `scores/baustoff-mill.de` | `conversion_probability` field unchanged |

### dataLayer.push()

```javascript
dataLayer.push({
  event: "purchase",
  page_path: "/v2/de/booking/express-1200-kg/test-repeat/confirmation",
  page_type: "booking_process",
  user_id: "test_first_order_baustoff-mill.de",
  company_name: "Test repeat",
  company_id: "",
  transaction_id: "TEST-phase3-repeat",
  value: 400,
  value_eur: 400,
  tax: 76,
  currency: "EUR",
  payment_type: "invoice",
  order_origin: "online",
  items: [
    {
      item_id: "11",
      item_name: "Small van",
      price: 400,
      quantity: 1,
      item_list_name: "express_main_products",
      index: 1,
      item_category: "express",
      loading_location: "DE_10115_Berlin",
      unloading_location: "DE_80331_Munich",
      loading_day: "24-03-2026",
      unloading_day: "24-03-2026",
      distance: 585,
      stopover: "FALSE"
    }
  ]
});
```

---
