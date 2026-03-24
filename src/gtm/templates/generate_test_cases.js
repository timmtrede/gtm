/**
 * Generate test cases for sGTM scoring validation.
 * Source: 5 rows from ml.company_scoring_data_v4
 *
 * Run: node src/gtm/templates/generate_test_cases.js
 *
 * Outputs for each test case:
 *   1. Expected probability, multiplier, label (from our JS model)
 *   2. A dataLayer JSON payload to simulate in GTM Preview
 *
 * JIRA: DATA-375
 */

var model = require("./scoring_model_v4");

// ============================================================
// 5 test rows from ml.company_scoring_data_v4
// ============================================================
// ============================================================
// 10 test cases: Firestore data (company profile + NACE) merged with
// BQ event data (revenue, distance, vehicle, payment, language, countries).
// The sGTM template reads Firestore for domain features and event data
// for transaction features, so this mirrors exactly what sGTM sees.
// ============================================================
var TEST_ROWS = [
  { name: "Case 1: Express, invoice, DE->DE, b2b+manufactures",
    // Firestore: old format, no nace_codes
    firestore: {"domain":"baustoff-mill.de","nace_codes":null,"no_shipping_required":false,"b2b_business_model":true,"logistics_transportation":true,"min_200_employees":"unknown","non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":true,"operates_europe_wide":false,"manufactures_product":true,"mainly_b2c":false,"high_quality_physical_goods":true,"low_cost_consumer_products":false},
    event: {"online":true,"payment_method":"invoice","net_revenue_first_transport":178.07,"distance_first_transport":95,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Small van","shipper_language":"de","loading_country_code":"DE","unloading_country_code":"DE"} },
  { name: "Case 2: Express, creditcard, AT->DE, no_shipping_required",
    // Firestore: new format, nace j+m
    firestore: {"domain":"alaika-advisory.com","nace_codes":"[\"70.2\",\"62.2\",\"62.9\"]","no_shipping_required":true,"b2b_business_model":true,"logistics_transportation":false,"min_200_employees":"unknown","non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":false,"operates_europe_wide":true,"manufactures_product":false,"mainly_b2c":false,"high_quality_physical_goods":false,"low_cost_consumer_products":false},
    event: {"online":true,"payment_method":"creditcard","net_revenue_first_transport":189.57,"distance_first_transport":125,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Small van","shipper_language":"de","loading_country_code":"AT","unloading_country_code":"DE"} },
  { name: "Case 3: Full truck, invoice, DE->DE, NACE c, 3.2t",
    // Firestore: new format, nace c (25.5, 25.9)
    firestore: {"domain":"nitec-zerspanung.de","nace_codes":"[\"25.5\",\"25.9\"]","no_shipping_required":false,"b2b_business_model":true,"logistics_transportation":true,"min_200_employees":false,"non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":false,"operates_europe_wide":false,"manufactures_product":true,"mainly_b2c":false,"high_quality_physical_goods":true,"low_cost_consumer_products":false},
    event: {"online":null,"payment_method":"invoice","net_revenue_first_transport":327.57,"distance_first_transport":237,"transport_type_first_transport":"full_truck_24_t","vehicle_type_first_transport":"3,2t Shipment","shipper_language":"de","loading_country_code":"DE","unloading_country_code":"DE"} },
  { name: "Case 4: Express, paypal, NL->BE, low_cost_consumer",
    // Firestore: old format, no nace_codes
    firestore: {"domain":"biscuits-bofin.be","nace_codes":null,"no_shipping_required":false,"b2b_business_model":false,"logistics_transportation":false,"min_200_employees":false,"non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":false,"operates_europe_wide":false,"manufactures_product":true,"mainly_b2c":true,"high_quality_physical_goods":false,"low_cost_consumer_products":true},
    event: {"online":true,"payment_method":"paypal","net_revenue_first_transport":226.86,"distance_first_transport":124,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Large van","shipper_language":"nl","loading_country_code":"NL","unloading_country_code":"BE"} },
  { name: "Case 5: Full truck 24t, invoice, DE->DE, NO profile",
    // Firestore: minimal doc, all profile fields null
    firestore: {"domain":"lewa-system.de","nace_codes":null,"no_shipping_required":null,"b2b_business_model":null,"logistics_transportation":null,"min_200_employees":null,"non_eu_operations":null,"turnover_10m_to_500m_eur":null,"heavy_large_products":null,"operates_europe_wide":null,"manufactures_product":null,"mainly_b2c":null,"high_quality_physical_goods":null,"low_cost_consumer_products":null},
    event: {"online":true,"payment_method":"invoice","net_revenue_first_transport":601.74,"distance_first_transport":170,"transport_type_first_transport":"full_truck_24_t","vehicle_type_first_transport":"24t Shipment","shipper_language":"de","loading_country_code":"DE","unloading_country_code":"DE"} },
  { name: "Case 6: Express, bancontact, BE->BE, NACE f",
    // Firestore: new format, nace f (43.2, 43.9)
    firestore: {"domain":"bumacogroup.be","nace_codes":"[\"43.2\",\"43.9\"]","no_shipping_required":false,"b2b_business_model":true,"logistics_transportation":false,"min_200_employees":true,"non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":false,"operates_europe_wide":false,"manufactures_product":false,"mainly_b2c":false,"high_quality_physical_goods":"unknown","low_cost_consumer_products":false},
    event: {"online":true,"payment_method":"bancontact","net_revenue_first_transport":114.7,"distance_first_transport":105,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Small van","shipper_language":"nl","loading_country_code":"BE","unloading_country_code":"BE"} },
  { name: "Case 7: Express, klarna, DE->DE, Large van, NO profile",
    // Firestore: new_scoring_error, all profile fields null
    firestore: {"domain":"proflextex.de","nace_codes":null,"no_shipping_required":null,"b2b_business_model":null,"logistics_transportation":null,"min_200_employees":null,"non_eu_operations":null,"turnover_10m_to_500m_eur":null,"heavy_large_products":null,"operates_europe_wide":null,"manufactures_product":null,"mainly_b2c":null,"high_quality_physical_goods":null,"low_cost_consumer_products":null},
    event: {"online":true,"payment_method":"klarna","net_revenue_first_transport":442.38,"distance_first_transport":344,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Large van","shipper_language":"de","loading_country_code":"DE","unloading_country_code":"DE"} },
  { name: "Case 8: Full truck, creditcard, PL->DE, cross-border",
    // Firestore: new format, nace f+m (42.2, 42.9, 43.2, 43.9, 71.1)
    firestore: {"domain":"skyline-energy.pl","nace_codes":"[\"42.2\",\"42.9\",\"43.2\",\"43.9\",\"71.1\"]","no_shipping_required":false,"b2b_business_model":true,"logistics_transportation":false,"min_200_employees":"unknown","non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":true,"operates_europe_wide":true,"manufactures_product":true,"mainly_b2c":false,"high_quality_physical_goods":true,"low_cost_consumer_products":false},
    event: {"online":true,"payment_method":"creditcard","net_revenue_first_transport":1599.75,"distance_first_transport":1200,"transport_type_first_transport":"full_truck_24_t","vehicle_type_first_transport":"3,2t Shipment","shipper_language":"pl","loading_country_code":"PL","unloading_country_code":"DE"} },
  { name: "Case 9: Express, ideal, NL->NL, Medium van",
    // Firestore: new format, nace j+m (62.1, 62.2, 62.9, 70.2, 73.1, 73.2, 73.3)
    firestore: {"domain":"happyhorizon.com","nace_codes":"[\"62.1\",\"62.2\",\"62.9\",\"70.2\",\"73.1\",\"73.2\",\"73.3\"]","no_shipping_required":true,"b2b_business_model":true,"logistics_transportation":false,"min_200_employees":true,"non_eu_operations":false,"turnover_10m_to_500m_eur":"unknown","heavy_large_products":false,"operates_europe_wide":false,"manufactures_product":false,"mainly_b2c":false,"high_quality_physical_goods":false,"low_cost_consumer_products":false},
    event: {"online":true,"payment_method":"ideal","net_revenue_first_transport":130.3,"distance_first_transport":111,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Medium van","shipper_language":"nl","loading_country_code":"NL","unloading_country_code":"NL"} },
  { name: "Case 10: Express, invoice, FR->FR, Medium van, NO profile",
    // Firestore: minimal doc, all profile fields null
    firestore: {"domain":"meca-sud.fr","nace_codes":null,"no_shipping_required":null,"b2b_business_model":null,"logistics_transportation":null,"min_200_employees":null,"non_eu_operations":null,"turnover_10m_to_500m_eur":null,"heavy_large_products":null,"operates_europe_wide":null,"manufactures_product":null,"mainly_b2c":null,"high_quality_physical_goods":null,"low_cost_consumer_products":null},
    event: {"online":true,"payment_method":"invoice","net_revenue_first_transport":334.22,"distance_first_transport":350,"transport_type_first_transport":"express_1200_kg","vehicle_type_first_transport":"Medium van","shipper_language":"fr","loading_country_code":"FR","unloading_country_code":"FR"} }
];

// ============================================================
// Vehicle type -> item_id reverse mapping
// ============================================================
var VEHICLE_TO_ITEM_ID = {
  "Large van": "0", "Tail lift and pallet truck": "1",
  "Length 450cm loading space": "2", "Length 480cm loading space": "3",
  "Width 220cm loading space": "4", "Width 230cm loading space": "5",
  "Loading from above": "8", "Dangerous Goods": "9", "Cooling-vehicle": "10",
  "Small van": "11", "Medium van": "12",
  "24t Shipment": "13", "2,4t Shipment": "14", "5t Shipment": "15",
  "12t Shipment": "16", "3,2t Shipment": "17", "1t Shipment": "18"
};

// ============================================================
// Process each test case
// ============================================================
var allCases = [];
TEST_ROWS.forEach(function(tc) {
  var fs = tc.firestore; // Firestore scores document (what sGTM reads)
  var ev = tc.event;     // Event data (what we control in test payload)

  // Build features exactly as the sGTM template would
  var features = {};

  // Company profile from Firestore (toModelString converts bool->string)
  var profileFields = [
    "no_shipping_required", "b2b_business_model", "logistics_transportation",
    "min_200_employees", "non_eu_operations", "turnover_10m_to_500m_eur",
    "heavy_large_products", "operates_europe_wide", "manufactures_product",
    "mainly_b2c", "high_quality_physical_goods", "low_cost_consumer_products"
  ];
  profileFields.forEach(function(f) {
    features[f] = model.toModelString(fs[f]);
  });

  // NACE one-hot from Firestore nace_codes
  var naceOneHot = model.parseNaceCodes(fs.nace_codes);
  for (var letter in naceOneHot) {
    features[letter] = naceOneHot[letter];
  }

  // Event data features — derive exactly as the sGTM template does
  features.net_revenue_first_transport = ev.net_revenue_first_transport;
  features.distance_first_transport = ev.distance_first_transport;
  features.transport_type_first_transport = ev.transport_type_first_transport;
  features.vehicle_type_first_transport = ev.vehicle_type_first_transport;
  features.payment_method = ev.payment_method;
  features.shipper_language = ev.shipper_language;
  features.loading_country_code = ev.loading_country_code;
  features.unloading_country_code = ev.unloading_country_code;
  features.tld = model.extractTld(fs.domain);

  // online: In production, front-end always sends order_origin ("online"/"offline").
  // BQ training data has online=null for some rows, but sGTM never sees null.
  // For test validation, use what sGTM will actually receive:
  //   BQ true  → order_origin="online"  → sGTM online="true"
  //   BQ false → order_origin="offline" → sGTM online="false"
  //   BQ null  → order_origin="offline" → sGTM online="false" (production default)
  features.online = ev.online === true ? "true" : "false";
  var onlineDiscrepancy = (ev.online === null || ev.online === undefined);

  var d = ev; // for payload generation below

  // Compute expected outputs
  var prob = model.predictConversionProbability(features);
  var mult = model.computeMultiplier(prob);
  var adjValue = model.calculateAdjustedValue(prob, d.net_revenue_first_transport);
  var label = model.getMonitoringLabel(prob);
  var gadsLabel = model.getGadsLabel(prob);

  // Build item_id from vehicle type
  var itemId = VEHICLE_TO_ITEM_ID[ev.vehicle_type_first_transport] || "0";
  var itemCategory = ev.transport_type_first_transport === "full_truck_24_t" ? "lkw" : "express";
  var itemListName = itemCategory === "lkw" ? "lkw_main_products" : "express_main_products";
  var transportSlug = ev.transport_type_first_transport === "full_truck_24_t" ? "full-truck-24-t" : "express-1200-kg";
  var lang = ev.shipper_language || "de";

  // Build dataLayer payload
  var payload = {
    page_type: "booking_process",
    page_path: "/v2/" + lang + "/booking/" + transportSlug + "/test-" + fs.domain + "/confirmation",
    event: "purchase",
    user_id: "test_v3_" + fs.domain,
    company_name: "Test " + fs.domain,
    transaction_id: "TEST-" + fs.domain.replace(/\./g, "-"),
    value: d.net_revenue_first_transport,
    value_eur: d.net_revenue_first_transport,
    tax: Math.round(d.net_revenue_first_transport * 0.19 * 100) / 100,
    currency: "EUR",
    payment_type: d.payment_method,
    order_origin: ev.online === true ? "online" : "offline",
    items: [{
      item_id: itemId,
      item_name: d.vehicle_type_first_transport,
      price: d.net_revenue_first_transport,
      price_eur: d.net_revenue_first_transport,
      quantity: 1,
      item_list_name: itemListName,
      item_category: itemCategory,
      loading_location: d.loading_country_code + "_10115_Test City",
      unloading_location: d.unloading_country_code + "_20095_Test Destination",
      distance: Math.round(d.distance_first_transport),
      stopover: false
    }]
  };

  // Build dataLayer.push() snippet matching user's format
  var loadingDay = new Date().toLocaleDateString("en-GB", {day: "2-digit", month: "2-digit", year: "numeric"}).replace(/\//g, "-");
  var dlPush = "dataLayer.push({\n"
    + '  event: "purchase",\n'
    + '  page_path: "' + payload.page_path + '",\n'
    + '  page_type: "' + payload.page_type + '",\n'
    + '  user_id: "test_v3_' + fs.domain + '",\n'
    + '  company_name: "Test ' + fs.domain + '",\n'
    + '  company_id: "",\n'
    + '  transaction_id: "' + payload.transaction_id + '",\n'
    + '  value: ' + payload.value + ',\n'
    + '  value_eur: ' + payload.value_eur + ',\n'
    + '  tax: ' + payload.tax + ',\n'
    + '  currency: "EUR",\n'
    + '  payment_type: "' + payload.payment_type + '",\n'
    + '  order_origin: "' + payload.order_origin + '",\n'
    + '  items: [\n'
    + '    {\n'
    + '      item_id: "' + itemId + '",\n'
    + '      item_name: "' + d.vehicle_type_first_transport + '",\n'
    + '      price: ' + payload.value + ',\n'
    + '      quantity: 1,\n'
    + '      item_list_name: "' + itemListName + '",\n'
    + '      index: 1,\n'
    + '      item_category: "' + itemCategory + '",\n'
    + '      loading_location: "' + d.loading_country_code + '_10115_Test City",\n'
    + '      unloading_location: "' + d.unloading_country_code + '_20095_Test Destination",\n'
    + '      loading_day: "' + loadingDay + '",\n'
    + '      unloading_day: "' + loadingDay + '",\n'
    + '      distance: ' + Math.round(d.distance_first_transport) + ',\n'
    + '      stopover: "FALSE"\n'
    + '    }\n'
    + '  ]\n'
    + '});';

  // Collect for markdown output
  allCases.push({
    name: tc.name,
    domain: fs.domain,
    onlineDiscrepancy: onlineDiscrepancy,
    prob: prob.toFixed(6),
    mult: mult.toFixed(4),
    adjValue: adjValue,
    label: label,
    gadsLabel: gadsLabel,
    dlPush: dlPush
  });
});

// ============================================================
// Generate markdown
// ============================================================
var md = "# DATA-375 — sGTM Scoring Validation Test Cases\n\n";
md += "Generated: " + new Date().toISOString().split("T")[0] + "\n\n";
md += "## Prerequisites\n\n";
md += "For each test case:\n";
md += "1. Set cookie `ed` to the test domain (browser devtools or GTM Preview override)\n";
md += "2. Ensure the `user_id` is NOT in Firestore `existing_customers` (the test IDs are unique)\n";
md += "3. Ensure the domain is NOT in Firestore `generic_domains`\n";
md += "4. Ensure the domain IS in Firestore `scores` with matching profile data\n";
md += "5. Open server container GTM Preview, inject the `dataLayer.push()` snippet in the browser console\n\n";
md += "## Summary\n\n";
md += "| # | Domain | Probability | Multiplier | Label | Adjusted Value |\n";
md += "|---|--------|-------------|------------|-------|----------------|\n";
allCases.forEach(function(c, i) {
  md += "| " + (i+1) + " | `" + c.domain + "` | " + c.prob + " | " + c.mult + " | " + c.label + " | " + c.adjValue + " |\n";
});
md += "\n---\n\n";

allCases.forEach(function(c, i) {
  md += "## " + c.name + "\n\n";
  md += "**Domain:** `" + c.domain + "`\n";
  if (c.onlineDiscrepancy) {
    md += "\n> Note: BQ has `online=null` for this domain. In production, sGTM always receives `order_origin` (\"online\" or \"offline\"), so `online` is never null. Expected values below reflect production behavior (`online=\"false\"`).\n";
  }
  md += "\n";
  md += "### Expected Values\n\n";
  md += "| Variable | Expected Value |\n";
  md += "|----------|----------------|\n";
  md += "| `scoring.conversion_probability` | " + c.prob + " |\n";
  md += "| multiplier (`prob * 3`, clamped) | " + c.mult + " |\n";
  md += "| `scoring.adjusted_value` | " + c.adjValue + " |\n";
  md += "| `scoring.label` | `" + c.label + "` |\n";
  md += "| `alookup.gads_variable_label` | `" + c.gadsLabel + "` |\n\n";
  md += "### dataLayer.push()\n\n";
  md += "```javascript\n" + c.dlPush + "\n```\n\n";
  md += "---\n\n";
});

// Write to file
var fs = require("fs");
var outPath = __dirname + "/../../.." + "/specs/test-cases-scoring.md";
fs.writeFileSync(outPath, md);
console.log("Written to: specs/test-cases-scoring.md");
console.log(allCases.length + " test cases generated.");
