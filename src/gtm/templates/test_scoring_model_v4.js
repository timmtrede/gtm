/**
 * Tests for Company Scoring v4 model
 * Run: node test_scoring_model_v4.js
 */

var model = require("./scoring_model_v4");

var passed = 0;
var failed = 0;

function assert(condition, message) {
  if (condition) {
    passed++;
  } else {
    failed++;
    console.log("FAIL: " + message);
  }
}

function assertApprox(actual, expected, tolerance, message) {
  var diff = Math.abs(actual - expected);
  if (diff <= tolerance) {
    passed++;
  } else {
    failed++;
    console.log("FAIL: " + message + " (expected ~" + expected + ", got " + actual + ", diff " + diff + ")");
  }
}

// ============================================================
// Test: DATA-375 example from JIRA ticket
// ============================================================
console.log("\n--- DATA-375 Example ---");
var exampleProb = model.predictConversionProbability({
  no_shipping_required: "false",
  b2b_business_model: "true",
  logistics_transportation: "false",
  min_200_employees: "unknown",
  non_eu_operations: "false",
  turnover_10m_to_500m_eur: "unknown",
  heavy_large_products: "false",
  operates_europe_wide: "true",
  manufactures_product: "true",
  mainly_b2c: "false",
  high_quality_physical_goods: "true",
  low_cost_consumer_products: "false",
  tld: ".de",
  online: "true",
  payment_method: "invoice",
  net_revenue_first_transport: 300,
  transport_type_first_transport: "express_1200_kg",
  vehicle_type_first_transport: "Large van",
  shipper_language: "de",
  loading_country_code: "DE",
  unloading_country_code: "DE",
  distance_first_transport: 250,
  a: 0, b: 0, c: 1, d: 0, e: 0, f: 0, g: 0, h: 0, i: 0, j: 0,
  k: 0, l: 0, m: 0, n: 0, o: 0, p: 0, q: 0, r: 0, s: 0, t: 0, u: 0
});
console.log("Example probability: " + exampleProb);
assert(exampleProb > 0 && exampleProb < 1, "Probability should be between 0 and 1");
assert(exampleProb > 0.3, "Example should have reasonable probability (>0.3)");

// ============================================================
// Test: Multiplier clamping (prob * 3, clamped to [0.6, 2.4])
// ============================================================
console.log("\n--- Multiplier ---");
assertApprox(model.computeMultiplier(0.1), 0.6, 0.001, "prob=0.1 -> 0.3 clamped to floor 0.6");
assertApprox(model.computeMultiplier(0.15), 0.6, 0.001, "prob=0.15 -> 0.45 clamped to floor 0.6");
assertApprox(model.computeMultiplier(0.2), 0.6, 0.001, "prob=0.2 -> 0.6 = floor");
assertApprox(model.computeMultiplier(0.3), 0.9, 0.001, "prob=0.3 -> 0.9");
assertApprox(model.computeMultiplier(0.5), 1.5, 0.001, "prob=0.5 -> 1.5");
assertApprox(model.computeMultiplier(0.8), 2.4, 0.001, "prob=0.8 -> 2.4 = cap");
assertApprox(model.computeMultiplier(0.9), 2.4, 0.001, "prob=0.9 -> 2.7 clamped to cap 2.4");
assertApprox(model.computeMultiplier(0.99), 2.4, 0.001, "prob=0.99 -> clamped to cap 2.4");

// ============================================================
// Test: Value formula (JIRA examples with factor 3)
// ============================================================
console.log("\n--- Value Formula ---");
assertApprox(model.calculateAdjustedValue(0.5, 1000), 1500, 0.01, "prob=0.5 -> 1.5*1000=1500 (JIRA ex1)");
assertApprox(model.calculateAdjustedValue(0.1, 1000), 600, 0.01, "prob=0.1 -> floor 0.6*1000=600 (JIRA ex2)");
assertApprox(model.calculateAdjustedValue(0.9, 1000), 2400, 0.01, "prob=0.9 -> cap 2.4*1000=2400 (JIRA ex3)");
assertApprox(model.calculateAdjustedValue(0.0, 500), 300, 0.01, "prob=0 -> floor 0.6*500=300");
assertApprox(model.calculateAdjustedValue(0.4, 500), 600, 0.01, "prob=0.4 -> 1.2*500=600");
assertApprox(model.calculateAdjustedValue(0.8, 500), 1200, 0.01, "prob=0.8 -> cap 2.4*500=1200");

// ============================================================
// Test: Monitoring labels (based on multiplier buckets)
// ============================================================
console.log("\n--- Monitoring Labels ---");
// B-Kunden: multiplier < 0.8 (prob < 0.267)
assert(model.getMonitoringLabel(0.1) === "b_kunden", "prob=0.1 -> mult=0.6 -> b_kunden");
assert(model.getMonitoringLabel(0.2) === "b_kunden", "prob=0.2 -> mult=0.6 -> b_kunden");
assert(model.getMonitoringLabel(0.25) === "b_kunden", "prob=0.25 -> mult=0.75 -> b_kunden");
// A-Kunden: 0.8 <= multiplier <= 1.2 (prob 0.267 - 0.4)
assert(model.getMonitoringLabel(0.3) === "a_kunden", "prob=0.3 -> mult=0.9 -> a_kunden");
assert(model.getMonitoringLabel(0.35) === "a_kunden", "prob=0.35 -> mult=1.05 -> a_kunden");
assert(model.getMonitoringLabel(0.4) === "a_kunden", "prob=0.4 -> mult=1.2 -> a_kunden");
// A+ Kunden: multiplier > 1.2 (prob > 0.4)
assert(model.getMonitoringLabel(0.41) === "a_plus_kunden", "prob=0.41 -> mult=1.23 -> a_plus_kunden");
assert(model.getMonitoringLabel(0.5) === "a_plus_kunden", "prob=0.5 -> mult=1.5 -> a_plus_kunden");
assert(model.getMonitoringLabel(0.9) === "a_plus_kunden", "prob=0.9 -> mult=2.4(cap) -> a_plus_kunden");

// ============================================================
// Test: Google Ads labels
// ============================================================
console.log("\n--- Google Ads Labels ---");
assert(model.getGadsLabel(0.1) === "kIETCImEtuYaEObk9sED", "B-Kunden label");
assert(model.getGadsLabel(0.35) === "5PHlCJX_qOYaEObk9sED", "A-Kunden label");
assert(model.getGadsLabel(0.5) === "2JWlCIOsqIwcEObk9sED", "A+ Kunden label");

// ============================================================
// Test: NACE code parsing
// ============================================================
console.log("\n--- NACE Parsing ---");
var nace1 = model.parseNaceCodes('["49.4","50.2","52.2"]');
assert(nace1.h === 1, 'NACE ["49.4","50.2","52.2"] -> h=1 (all section H)');
assert(nace1.a === 0, 'NACE ["49.4","50.2","52.2"] -> a=0');
assert(nace1.c === 0, 'NACE ["49.4","50.2","52.2"] -> c=0');

var nace2 = model.parseNaceCodes('["25.1","49.4"]');
assert(nace2.c === 1, 'NACE ["25.1","49.4"] -> c=1 (25 is manufacturing)');
assert(nace2.h === 1, 'NACE ["25.1","49.4"] -> h=1 (49 is transport)');

var nace3 = model.parseNaceCodes('["58.1"]');
assert(nace3.j === 1, 'NACE ["58.1"] -> j=1 (58 is publishing/J)');

var nace4 = model.parseNaceCodes(null);
var allZero = true;
for (var k in nace4) { if (nace4[k] !== 0) allZero = false; }
assert(allZero, "NACE null -> all zeros");

var nace5 = model.parseNaceCodes('[]');
allZero = true;
for (var k2 in nace5) { if (nace5[k2] !== 0) allZero = false; }
assert(allZero, "NACE empty array -> all zeros");

var nace6 = model.parseNaceCodes('["47.4","62.2","62.9","63.1"]');
assert(nace6.g === 1, 'NACE with 47 -> g=1 (wholesale/retail)');
assert(nace6.j === 1, 'NACE with 62,63 -> j=1 (IT/publishing)');

// ============================================================
// Test: Vehicle type mapping
// ============================================================
console.log("\n--- Vehicle Type Mapping ---");
assert(model.VEHICLE_TYPE_MAP["0"] === "Large van", "item_id 0 -> Large van");
assert(model.VEHICLE_TYPE_MAP["11"] === "Small van", "item_id 11 -> Small van");
assert(model.VEHICLE_TYPE_MAP["12"] === "Medium van", "item_id 12 -> Medium van");
assert(model.VEHICLE_TYPE_MAP["17"] === "3,2t Shipment", "item_id 17 -> 3,2t Shipment");
assert(model.VEHICLE_TYPE_MAP["7"] === "Large van", "item_id 7 (Overhang) -> Large van");
assert(model.VEHICLE_TYPE_MAP["10"] === "Large van", "item_id 10 (Cooling) -> Large van");
assert(model.VEHICLE_TYPE_MAP["6"] === null, "item_id 6 (Ramp height) -> null");
assert(model.VEHICLE_TYPE_MAP["18"] === null, "item_id 18 (1t) -> null");

// ============================================================
// Test: TLD extraction
// ============================================================
console.log("\n--- TLD Extraction ---");
assert(model.extractTld("example.de") === ".de", "example.de -> .de");
assert(model.extractTld("company.co.uk") === ".uk", "company.co.uk -> .uk");
assert(model.extractTld("test.com") === ".com", "test.com -> .com");
assert(model.extractTld(null) === null, "null -> null");
assert(model.extractTld("nodot") === null, "nodot -> null");

// ============================================================
// Test: Language extraction
// ============================================================
console.log("\n--- Language Extraction ---");
assert(model.extractLanguage("/v2/de/booking/express-1200-kg/123/confirmation") === "de", "page_path de");
assert(model.extractLanguage("/v2/en/payment/abc") === "en", "page_path en");
assert(model.extractLanguage("/v2/fr/booking/full-truck-24-t/456/confirmation") === "fr", "page_path fr");
assert(model.extractLanguage(null) === null, "null page_path");
assert(model.extractLanguage("/other/path") === null, "non-v2 path");

// ============================================================
// Test: Country code extraction
// ============================================================
console.log("\n--- Country Code Extraction ---");
assert(model.extractCountryCode("DE_68199_Mannheim") === "DE", "DE_68199_Mannheim -> DE");
assert(model.extractCountryCode("FR_75001_Paris") === "FR", "FR_75001_Paris -> FR");
assert(model.extractCountryCode("GB_CA25 5HU_Cleator Moor") === "GB", "GB format");
assert(model.extractCountryCode(null) === null, "null -> null");
assert(model.extractCountryCode("X") === null, "too short -> null");

// ============================================================
// Test: toModelString conversion
// ============================================================
console.log("\n--- Boolean to Model String ---");
assert(model.toModelString(true) === "true", "bool true -> 'true'");
assert(model.toModelString(false) === "false", "bool false -> 'false'");
assert(model.toModelString("unknown") === "unknown", "string unknown -> 'unknown'");
assert(model.toModelString("true") === "true", "string true -> 'true'");
assert(model.toModelString(null) === null, "null -> null");
assert(model.toModelString(undefined) === null, "undefined -> null");

// ============================================================
// Test: buildFeatures with sample data
// ============================================================
console.log("\n--- buildFeatures ---");
var sampleScoresDoc = {
  domain: "testcompany.de",
  no_shipping_required: false,
  b2b_business_model: true,
  logistics_transportation: false,
  min_200_employees: "unknown",
  non_eu_operations: false,
  turnover_10m_to_500m_eur: "unknown",
  heavy_large_products: false,
  operates_europe_wide: true,
  manufactures_product: true,
  mainly_b2c: false,
  high_quality_physical_goods: true,
  low_cost_consumer_products: false,
  nace_codes: '["25.1","49.4"]'
};

var sampleEventData = {
  value_eur: 258.13,
  value: 258.13,
  payment_type: "invoice",
  order_origin: "online",
  page_path: "/v2/de/booking/express-1200-kg/69bab58115bab0ec1009dcef/confirmation"
};

var sampleMainItem = {
  item_id: "11",
  item_name: "Kleiner Transporter",
  item_category: "express",
  item_list_name: "express_main_products",
  distance: 267,
  loading_location: "DE_22041_Hamburg",
  unloading_location: "DE_33014_Bad Driburg"
};

var features = model.buildFeatures(sampleScoresDoc, sampleEventData, sampleMainItem);
assert(features.no_shipping_required === "false", "Profile: no_shipping_required=false");
assert(features.b2b_business_model === "true", "Profile: b2b_business_model=true");
assert(features.min_200_employees === "unknown", "Profile: min_200_employees=unknown");
assert(features.c === 1, "NACE: 25 -> c=1");
assert(features.h === 1, "NACE: 49 -> h=1");
assert(features.a === 0, "NACE: a=0 (not present)");
assert(features.net_revenue_first_transport === 258.13, "Revenue: 258.13 EUR");
assert(features.distance_first_transport === 267, "Distance: 267");
assert(features.transport_type_first_transport === "express_1200_kg", "Transport: express -> express_1200_kg");
assert(features.vehicle_type_first_transport === "Small van", "Vehicle: item_id 11 -> Small van");
assert(features.online === "true", "Online: true");
assert(features.payment_method === "invoice", "Payment: invoice");
assert(features.shipper_language === "de", "Language: de");
assert(features.loading_country_code === "DE", "Loading: DE");
assert(features.unloading_country_code === "DE", "Unloading: DE");
assert(features.tld === ".de", "TLD: .de");

// Run the model with built features
var builtProb = model.predictConversionProbability(features);
console.log("Built features probability: " + builtProb);
assert(builtProb > 0 && builtProb < 1, "Built features probability in range");

// ============================================================
// Test: Model with all nulls (should still work with mean values)
// ============================================================
console.log("\n--- All Nulls ---");
var nullProb = model.predictConversionProbability({});
console.log("All null features probability: " + nullProb);
assert(nullProb > 0 && nullProb < 1, "All nulls probability in range");

// ============================================================
// Test: Case insensitivity
// ============================================================
console.log("\n--- Case Insensitivity ---");
var upperFeatures = Object.assign({}, features);
upperFeatures.payment_method = "INVOICE";
var upperProb = model.predictConversionProbability(upperFeatures);
assert(Math.abs(upperProb - builtProb) < 0.001, "Case insensitive: INVOICE == invoice");

// ============================================================
// Summary
// ============================================================
console.log("\n==================");
console.log("Passed: " + passed + ", Failed: " + failed);
if (failed > 0) {
  process.exit(1);
} else {
  console.log("All tests passed!");
}
