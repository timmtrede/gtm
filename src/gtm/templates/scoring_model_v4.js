/**
 * Company Scoring v4 — Logistic Regression Model
 * Predicts probability of a domain placing 3+ orders.
 *
 * Model: zipmend-2e643.ml.company_scoring_v4
 * JIRA: DATA-375
 *
 * This file contains the pure model logic, usable both:
 * - In Node.js for testing
 * - Adapted for sGTM sandboxed JS template
 */

// ============================================================
// NACE DIVISION-TO-SECTION MAPPING
// Maps numeric NACE division codes to section letters (a-u)
// ============================================================
var NACE_DIVISION_TO_SECTION = {
  1: "a", 2: "a", 3: "a",
  5: "b", 6: "b", 7: "b", 8: "b", 9: "b",
  10: "c", 11: "c", 12: "c", 13: "c", 14: "c", 15: "c", 16: "c",
  17: "c", 18: "c", 19: "c", 20: "c", 21: "c", 22: "c", 23: "c",
  24: "c", 25: "c", 26: "c", 27: "c", 28: "c", 29: "c", 30: "c",
  31: "c", 32: "c", 33: "c",
  35: "d",
  36: "e", 37: "e", 38: "e", 39: "e",
  41: "f", 42: "f", 43: "f",
  45: "g", 46: "g", 47: "g",
  49: "h", 50: "h", 51: "h", 52: "h", 53: "h",
  55: "i", 56: "i",
  58: "j", 59: "j", 60: "j", 61: "j", 62: "j", 63: "j",
  64: "k", 65: "k", 66: "k",
  68: "l",
  69: "m", 70: "m", 71: "m", 72: "m", 73: "m", 74: "m", 75: "m",
  77: "n", 78: "n", 79: "n", 80: "n", 81: "n", 82: "n",
  84: "o",
  85: "p",
  86: "q", 87: "q", 88: "q",
  90: "r", 91: "r", 92: "r", 93: "r",
  94: "s", 95: "s", 96: "s",
  97: "t", 98: "t",
  99: "u"
};

// ============================================================
// VEHICLE TYPE MAPPING (item_id STRING -> model weight key)
// Source: dm_stg.stg_mapping_vehicle_type_labels
// ============================================================
var VEHICLE_TYPE_MAP = {
  "0": "Large van",
  "1": "Tail lift and pallet truck",
  "2": "Length 450cm loading space",
  "3": "Length 480cm loading space",
  "4": "Width 220cm loading space",
  "5": "Width 230cm loading space",
  "6": null,                          // Ramp height — not in model
  "7": "Large van",                   // Overhang — mapped to big van
  "8": "Loading from above",
  "9": "Dangerous Goods",
  "10": "Large van",                  // Cooling-vehicle — mapped to big van
  "11": "Small van",
  "12": "Medium van",
  "13": "24t Shipment",
  "14": "2,4t Shipment",
  "15": "5t Shipment",
  "16": "12t Shipment",
  "17": "3,2t Shipment",
  "18": null                          // 1t Shipment — not in model
};

// ============================================================
// TRANSPORT TYPE MAPPING (item_category -> model key)
// ============================================================
var TRANSPORT_TYPE_MAP = {
  "express": "express_1200_kg",
  "lkw": "full_truck_24_t"
};

// ============================================================
// MODEL WEIGHTS — company_scoring_v4
// ============================================================
var INTERCEPT = 0.19609285288872272;

var NUMERIC_FEATURES = {
  net_revenue_first_transport: { weight: 1.107061766784912e-5, mean: 366.1414280793821, stddev: 321.82600082883715 },
  distance_first_transport:    { weight: 6.323441850322997e-5, mean: 316.16649780479764, stddev: 320.1420009659045 },
  a: { weight: -0.3724418399822121,  mean: 0.007880220646178123, stddev: 0.08842512646147806 },
  b: { weight: -0.06417412913497608, mean: 0.0020263424518743647, stddev: 0.044971814130477954 },
  c: { weight: -0.2632725211672573,  mean: 0.2289766970618035,   stddev: 0.4201978654581521 },
  d: { weight: -0.49517150148598943, mean: 0.006304176516942455, stddev: 0.07915263211543014 },
  e: { weight: -0.3233593619270897,  mean: 0.010919734323989686, stddev: 0.1039312740431183 },
  f: { weight: -0.31192458934273726, mean: 0.08656985252729928,  stddev: 0.2812195157802441 },
  g: { weight: -0.33773296920594353, mean: 0.11910390633794907,  stddev: 0.3239289710434889 },
  h: { weight: -0.1137643669608994,  mean: 0.03320950129460761,  stddev: 0.179193317720695 },
  i: { weight: -0.3504966677499206,  mean: 0.01531014296971746,  stddev: 0.12279022692555953 },
  j: { weight: -0.2760497540103016,  mean: 0.020038275357424258, stddev: 0.14013905139219598 },
  k: { weight: -0.26846351745026564, mean: 0.06022740065293277,  stddev: 0.2379210652906047 },
  l: { weight: -0.42024230124900225, mean: 0.01114488348530901,  stddev: 0.10498531252019136 },
  m: { weight: -0.4108003711413672,  mean: 0.01564786671169644,  stddev: 0.12411585378909575 },
  n: { weight: -0.298967049218506,   mean: 0.1794438815715416,   stddev: 0.38374516636764844 },
  o: { weight: -0.23946870367145703, mean: 0.05516154452324664,  stddev: 0.22830816112415636 },
  p: { weight: -0.44168843033004374, mean: 0.002701789935832494, stddev: 0.051911401755666726 },
  q: { weight: -0.31568583174643416, mean: 0.022965214454576104, stddev: 0.1498009999681272 },
  r: { weight: -0.32659569463848465, mean: 0.015422717550377125, stddev: 0.1232337898270804 },
  s: { weight: -0.39376798196052365, mean: 0.01879995497016775,  stddev: 0.13582559959729631 },
  t: { weight: -0.34740888783379653, mean: 0.016661037937633627, stddev: 0.12800504802501472 },
  u: { weight: -0.4716439511463671,  mean: 1.1257458065968654e-4, stddev: 0.01061011690132048 }
};

var CATEGORICAL_WEIGHTS = {
  no_shipping_required: {
    "false": 0.023170144583303243,
    "true": -0.2100050877451799,
    "unknown": -0.21668976294307804,
    _null: 0
  },
  b2b_business_model: {
    "false": -0.12742904380817627,
    "true": -0.03191401420500469,
    "unknown": -0.09014046223464109,
    _null: 0
  },
  logistics_transportation: {
    "false": -0.09141360555907964,
    "true": 0.15029359800121406,
    "unknown": -0.056748765001659054,
    _null: 0
  },
  min_200_employees: {
    "false": -0.20322449080190091,
    "true": -0.005473507280983768,
    "unknown": 0.01228560443283689,
    _null: 0
  },
  non_eu_operations: {
    "false": -0.05086572354888771,
    "true": -0.17450094987563347,
    "unknown": 0.004903253255952854,
    _null: 0
  },
  turnover_10m_to_500m_eur: {
    "false": -0.16150812880266724,
    "true": -0.09645440891765765,
    "unknown": -0.0449481513979897,
    _null: 0
  },
  heavy_large_products: {
    "false": -0.050820388714084494,
    "true": -0.062310795252904845,
    "unknown": 0.025326354673188205,
    _null: 0
  },
  operates_europe_wide: {
    "false": -0.1812178769217589,
    "true": 0.03169008753973013,
    "unknown": -0.05772174798582227,
    _null: 0
  },
  manufactures_product: {
    "false": -0.09135988284829209,
    "true": -0.01578573170173398,
    "unknown": -0.28816673660538455,
    _null: 0
  },
  mainly_b2c: {
    "false": -0.030404572212813043,
    "true": -0.11933925103442233,
    "unknown": -0.09323862402918759,
    _null: 0
  },
  high_quality_physical_goods: {
    "false": -0.08407194863374717,
    "true": -0.024769104380562765,
    "unknown": -0.1443110899430542,
    _null: 0
  },
  low_cost_consumer_products: {
    "false": -0.05565687419125419,
    "true": 0.05026151070673836,
    "unknown": -0.2820964795098649,
    "partial": -0.7191522565129611,
    _null: 0
  },
  online: {
    "true": -0.07541606842202789,
    "false": -0.5397222798605793,
    _null: 0.1062734370313775
  },
  payment_method: {
    "invoice": -5.93473779407494e-6,
    "creditcard": -0.16222340897896984,
    "paypal": 0.035444836044058126,
    "klarna": -0.4204481799079659,
    "bancontact": 0.32839560966525144,
    "ideal": -0.1318001141983648,
    "sofort": -0.4204481799079659, // mapped to klarna
    "advance_payment": 0.041069443765247904, // mapped to advancePayment
    "advance_payment_wise": 0.041069443765247904, // mapped to advancePayment
    "advancepayment": 0.041069443765247904,
    "przelewy24": -0.35585390151964036,
    "belfius": -0.8998594267255149,
    "billie": 0.046636753465026104,
    "trustly": 0, // deprecated, baseline
    _null: -0.35117487703131195
  },
  transport_type_first_transport: {
    "express_1200_kg": -0.07164918243729212,
    "full_truck_24_t": 0.07856094735676566,
    _null: 0.7314563562221194
  },
  vehicle_type_first_transport: {
    "loading from above": -1.0090647288605212,
    "overhang": -0.7455498019249021,
    "small van": -0.14500307813606342,
    "tail lift and pallet truck": -0.14619399492007565,
    "3,2t shipment": -0.01934229068327046,
    "dangerous goods": 0.009642811761652511,
    "12t shipment": 0.018337507885265166,
    "medium van": 0.0459485798505546,
    "width 230cm loading space": 0.19575835527804575,
    "2,4t shipment": 0.19739518683690896,
    "24t shipment": 0.18550335110407606,
    "width 220cm loading space": 0.20939917092622387,
    "large van": 0.2721545098397925,
    "5t shipment": 0.2785774636546063,
    "length 480cm loading space": 0.710275693059552,
    "length 450cm loading space": 0.9796427358149071,
    "cooling-vehicle": 1.5447771209066998,
    _null: 0.7314563562221194
  },
  shipper_language: {
    "cs": -0.2364902016064497,
    "da": -0.3346683179634214,
    "de": 0.012438440538666032,
    "en": 0.13408050154306417,
    "es": -0.3452472562353442,
    "fr": -0.18428981718833637,
    "it": -0.06614715935468193,
    "nl": -0.01332541076048741,
    "pl": -0.20107492818628617,
    _null: 0.9685348059675722
  },
  loading_country_code: {
    "at": 0.052630829955904554, "be": 0.05735337090407901, "bg": 0.33480260239603316,
    "ch": -0.3574806137560447, "cz": -0.3173167981151924, "de": 0.04981692174870813,
    "dk": -0.05756833928405996, "ee": 1.6664561937426199, "es": -0.2550982808619707,
    "fi": -1.1370994096132252, "fr": -0.19737740227039333, "gb": -0.20068450228647428,
    "hr": -0.9488181600180816, "hu": 1.7494432048512736, "it": -0.002189422835830118,
    "lu": 0.15605535818398883, "mc": -0.6497010563227194, "nl": -0.012654741663777988,
    "pl": -0.17030881838838308, "pt": -0.12912270582442836, "ro": 1.6041755370842918,
    "se": 0.13368900971362854, "si": -0.9384967242965124, "sk": 1.0830929558070248,
    _null: 0
  },
  unloading_country_code: {
    "at": -0.0317014617214245, "be": 0.05983985331793877, "bg": -0.8486482795862077,
    "ch": -0.3767013435373036, "cz": 0.006202220511354719, "de": 0.026212912128504465,
    "dk": 0.11522243470303177, "es": -0.23908724267652284, "fr": -0.1794292913251229,
    "gb": -0.20158088851896402, "hr": 0.3365195383612399, "hu": 0.7561582222746955,
    "it": 0.03336274722484016, "lt": 0.6462978594512653, "lu": 0.0014041763048870046,
    "lv": -0.9061673375654165, "mc": -0.8012708854025692, "nl": -0.004952206699566343,
    "pl": 0.019005906981966757, "pt": -0.3127772784489193, "se": 0.44609934458403266,
    "si": -0.21833161998479186, "sk": 0.2652945915113065,
    _null: 0
  },
  tld: {
    ".aero": 0.6502634152327026, ".ag": 0.43231921896807124, ".agency": -0.43272025552234,
    ".ai": -0.003480242253640681, ".amsterdam": 1.6635411026530031, ".app": -0.9066106295913593,
    ".ar": -0.7750471250959377, ".archi": -0.5841714708057819, ".art": 0.2000578279429108,
    ".at": 0.011254480084047003, ".be": 0.0863372067517017, ".beer": -0.7506684779687889,
    ".berlin": -0.7378980550621429, ".bg": -0.5909244364668889, ".bike": 2.010964308814818,
    ".bio": 0.1405543398750746, ".biz": 0.4677183633269249, ".business": -0.6692947386942757,
    ".ca": 0.6907320111323177, ".care": -0.9028522846729727, ".cat": -0.6400932794130567,
    ".cc": -0.2565745110372459, ".ch": -0.5283264692305081, ".cloud": 0.3962096117023705,
    ".club": -0.6893749533343131, ".cn": -9.229268777407734e-4, ".co": 0.20431015931105817,
    ".com": -0.010379525113181135, ".company": -1.0451816899599393, ".coop": -0.6194922106044662,
    ".cy": -1.0522807626814823, ".cz": 0.0943210264503995, ".de": -0.014812343825890235,
    ".dev": -0.6860838411964041, ".digital": 0.2833177654410286, ".dk": -0.1794531384982014,
    ".earth": -0.864697217848788, ".edu": -0.7194896096787968, ".education": 2.236703617326663,
    ".energy": -0.7540372823712933, ".es": -0.4074533293966866, ".eu": -0.0755346080155647,
    ".events": 1.9654708366935727, ".expert": -0.7001807355738416, ".financial": -0.6887683089338323,
    ".fr": -0.18171200489019243, ".games": -0.7432109768312829, ".gg": 0.7445236290687979,
    ".global": -0.335049632708224, ".gmbh": -0.38840974652938426, ".group": -0.09525267945323382,
    ".gy": 2.080688866267988, ".hamburg": -1.1426608439385233, ".health": 2.266421770939927,
    ".healthcare": -0.8013911108872812, ".hk": 2.116574893875189, ".house": 0.3902667121450253,
    ".hr": -1.102905004603688, ".hu": -0.9873772697158445, ".ie": -0.6956249677120364,
    ".il": -0.8360650644053133, ".immo": -0.6952253656488734, ".immobilien": -0.8849425235548725,
    ".inc": -0.8739548579564496, ".info": -0.20881474904244846, ".international": -0.950013394481779,
    ".io": -0.1035509052565893, ".it": -0.1700182247197127, ".jp": -1.1067170123396066,
    ".kids": -0.7874451645001229, ".koeln": 0.1503178082798481, ".kr": -0.8424260420274503,
    ".la": -0.8751055197428415, ".land": 2.2174524996750318, ".law": 1.1351007681882985,
    ".leclerc": -0.7168124104430251, ".legal": -0.8169801115155572, ".life": 1.1023738613580099,
    ".lt": -0.9141002834515117, ".lu": 0.11793852900880152, ".me": 0.3604704572123422,
    ".media": -0.8855566576466536, ".moe": -0.6606828879703097, ".ms": -1.0032318088061456,
    ".mt": -0.9149326628033754, ".mu": -0.6386508662976813, ".museum": -0.9810860397477745,
    ".net": 0.015709660000029952, ".network": -0.9633327887837395, ".nl": -0.09335686965367644,
    ".nrw": -0.852337666485662, ".nu": 2.200693569777098, ".one": -0.9889606992959515,
    ".online": 0.4673468705537943, ".org": -0.2113019316642931, ".ovh": 2.190815711655396,
    ".paris": -0.08475658204024497, ".pl": -0.19167977843929904, ".plus": 1.7319733799317678,
    ".pro": 0.12391740234793644, ".productions": 1.8290781870735, ".pt": -0.6882743760141289,
    ".re": -0.7577952550138694, ".ro": -0.7782520757696013, ".rocks": 1.9244633348698574,
    ".schule": -0.9657027394181049, ".se": -0.8600003156429166, ".sener": -0.9466059998572675,
    ".services": 1.6628783927922006, ".sg": -1.2047762744610424, ".shop": -0.6509377675601441,
    ".site": 1.7888001856603253, ".sk": -0.9561200261167013, ".so": -0.7410934618240594,
    ".solutions": 0.7827854883731726, ".space": -0.8072676611248851, ".store": -0.3112813482352293,
    ".studio": -0.1460479496218846, ".support": 1.851647914313975, ".systems": 1.7958456954592816,
    ".tax": 0.612356903477952, ".team": -0.6962709620072306, ".tech": 0.14310246195216092,
    ".tirol": 0.14109729788592063, ".tr": -0.9818934915094663, ".tv": -0.513953133495216,
    ".uk": -0.33012300882324114, ".us": -0.8929793032651698, ".vin": -0.7668210829912783,
    ".vision": -0.698272438322039, ".work": -0.7053453806108098, ".world": 1.7042873397678695,
    ".xyz": -0.6027411024499743,
    _null: 0
  }
};

// ============================================================
// HELPER FUNCTIONS
// ============================================================

/**
 * Parse NACE codes JSON string into one-hot letter columns.
 * Input: '["49.4","50.2","52.2"]' or null
 * Output: { a: 0, b: 0, ..., h: 1, ..., u: 0 }
 */
function parseNaceCodes(naceCodesStr) {
  var result = {};
  var letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u"];
  for (var i = 0; i < letters.length; i++) {
    result[letters[i]] = 0;
  }

  if (!naceCodesStr) return result;

  try {
    var codes = JSON.parse(naceCodesStr);
    if (!codes || !codes.length) return result;

    for (var j = 0; j < codes.length; j++) {
      var code = codes[j];
      var division = parseInt(code, 10); // "49.4" -> 49
      if (isNaN(division)) continue;
      var section = NACE_DIVISION_TO_SECTION[division];
      if (section) {
        result[section] = 1;
      }
    }
  } catch (e) {
    // Parse error — return all zeros
  }

  return result;
}

/**
 * Extract TLD from domain string.
 * Input: "example.de" -> ".de"
 * Input: "example.co.uk" -> ".uk" (last segment)
 */
function extractTld(domain) {
  if (!domain) return null;
  var lastDot = domain.lastIndexOf(".");
  if (lastDot < 0) return null;
  return domain.substring(lastDot).toLowerCase();
}

/**
 * Extract language code from page_path.
 * Input: "/v2/de/booking/..." -> "de"
 */
function extractLanguage(pagePath) {
  if (!pagePath) return null;
  var match = pagePath.match(/\/v2\/([a-z]{2})\//);
  return match ? match[1] : null;
}

/**
 * Extract country code (first 2 chars) from location string.
 * Input: "DE_68199_Mannheim" -> "DE"
 */
function extractCountryCode(location) {
  if (!location || location.length < 2) return null;
  return location.substring(0, 2).toUpperCase();
}

/**
 * Convert Firestore boolean/string to model string.
 * Firestore stores: true, false, "unknown"
 * Model expects: "true", "false", "unknown"
 */
function toModelString(val) {
  if (val === true) return "true";
  if (val === false) return "false";
  if (val === "unknown") return "unknown";
  if (val === "true") return "true";
  if (val === "false") return "false";
  return null;
}

// ============================================================
// CORE MODEL FUNCTION
// ============================================================

/**
 * Predict conversion probability using logistic regression.
 * @param {Object} features - Feature dictionary with all model inputs
 * @returns {number} Probability between 0 and 1
 */
function predictConversionProbability(features) {
  var z = INTERCEPT;

  // Numeric features (standardized)
  for (var numKey in NUMERIC_FEATURES) {
    var f = NUMERIC_FEATURES[numKey];
    var val = features[numKey] != null ? features[numKey] : f.mean;
    if (f.stddev > 0) {
      z += f.weight * (val - f.mean) / f.stddev;
    }
  }

  // Categorical features
  for (var catKey in CATEGORICAL_WEIGHTS) {
    var catVal = features[catKey] != null ? String(features[catKey]).toLowerCase() : null;
    var weights = CATEGORICAL_WEIGHTS[catKey];
    if (catVal === null || catVal === "null") {
      z += weights._null || 0;
    } else if (weights[catVal] != null) {
      z += weights[catVal];
    }
    // Unknown category -> weight 0 (implicit baseline)
  }

  // Sigmoid — same approximation as sGTM template
  // (Math.exp not available in sGTM sandboxed JS)
  // exp(x) = (1 + x/65536)^65536, accurate to ~6 decimal places
  var zc = z < -20 ? -20 : (z > 20 ? 20 : z);
  var ex = 1 + (-zc) / 65536;
  for (var step = 0; step < 16; step++) { ex = ex * ex; }
  var probability = 1 / (1 + ex);
  return probability;
}

/**
 * Compute the clamped multiplier: prob * 3, clamped to [0.6, 2.4].
 * @param {number} probability - Conversion probability (0-1)
 * @returns {number} Multiplier between 0.6 and 2.4
 */
function computeMultiplier(probability) {
  var multiplier = probability * 3;
  if (multiplier > 2.4) multiplier = 2.4;
  if (multiplier < 0.6) multiplier = 0.6;
  return multiplier;
}

/**
 * Apply the value adjustment formula.
 * multiplier = clamp(prob * 3, 0.6, 2.4)
 * adjusted_value = multiplier * revenue
 *
 * @param {number} probability - Conversion probability (0-1)
 * @param {number} revenue - Order revenue (EUR)
 * @returns {number} Adjusted value
 */
function calculateAdjustedValue(probability, revenue) {
  var multiplier = computeMultiplier(probability);
  return Math.round(multiplier * revenue * 100) / 100;
}

/**
 * Determine the monitoring label bucket based on the multiplier.
 * multiplier < 0.8  → B-Kunden
 * 0.8 <= mult <= 1.2 → A-Kunden
 * mult > 1.2        → A+ Kunden
 *
 * @param {number} probability - Conversion probability (0-1)
 * @returns {string} Label key for customer groups
 */
function getMonitoringLabel(probability) {
  var multiplier = computeMultiplier(probability);
  if (multiplier < 0.8) return "b_kunden";
  if (multiplier < 1.2 + 1e-9) return "a_kunden";
  return "a_plus_kunden";
}

/**
 * Get the Google Ads conversion label for the monitoring bucket.
 * @param {number} probability - Conversion probability (0-1)
 * @returns {string} Google Ads conversion label ID
 */
function getGadsLabel(probability) {
  var label = getMonitoringLabel(probability);
  var LABEL_MAP = {
    "b_kunden": "kIETCImEtuYaEObk9sED",
    "a_kunden": "5PHlCJX_qOYaEObk9sED",
    "a_plus_kunden": "2JWlCIOsqIwcEObk9sED"
  };
  return LABEL_MAP[label];
}

/**
 * Build features from Firestore scores document + event data.
 * This is the main orchestration function.
 *
 * @param {Object} scoresDoc - Firestore scores document
 * @param {Object} eventData - Event data from sGTM
 * @param {Object} mainItem - First items[] entry with item_list_name containing "main_products"
 * @returns {Object} Features dict ready for predictConversionProbability()
 */
function buildFeatures(scoresDoc, eventData, mainItem) {
  var features = {};

  // 1. Company profile from Firestore scores
  var profileFields = [
    "no_shipping_required", "b2b_business_model", "logistics_transportation",
    "min_200_employees", "non_eu_operations", "turnover_10m_to_500m_eur",
    "heavy_large_products", "operates_europe_wide", "manufactures_product",
    "mainly_b2c", "high_quality_physical_goods", "low_cost_consumer_products"
  ];
  for (var i = 0; i < profileFields.length; i++) {
    var field = profileFields[i];
    features[field] = toModelString(scoresDoc[field]);
  }

  // 2. NACE one-hot from Firestore nace_codes
  var naceOneHot = parseNaceCodes(scoresDoc.nace_codes);
  for (var letter in naceOneHot) {
    features[letter] = naceOneHot[letter];
  }

  // 3. Revenue (EUR)
  features.net_revenue_first_transport = eventData.value_eur || eventData.value || null;

  // 4. Distance from items
  features.distance_first_transport = mainItem ? mainItem.distance : null;
  if (features.distance_first_transport != null) {
    features.distance_first_transport = Number(features.distance_first_transport);
  }

  // 5. Transport type from item_category
  var rawTransportType = mainItem ? mainItem.item_category : null;
  features.transport_type_first_transport = rawTransportType ? (TRANSPORT_TYPE_MAP[rawTransportType.toLowerCase()] || null) : null;

  // 6. Vehicle type from item_id
  var itemId = mainItem ? String(mainItem.item_id) : null;
  features.vehicle_type_first_transport = itemId ? (VEHICLE_TYPE_MAP[itemId] !== undefined ? VEHICLE_TYPE_MAP[itemId] : null) : null;

  // 7. Online flag from order_origin
  var orderOrigin = eventData.order_origin;
  features.online = orderOrigin === "online" ? "true" : (orderOrigin ? "false" : null);

  // 8. Payment method
  features.payment_method = eventData.payment_type || null;

  // 9. Language from page_path
  features.shipper_language = extractLanguage(eventData.page_path);

  // 10. Country codes from items
  features.loading_country_code = mainItem ? extractCountryCode(mainItem.loading_location) : null;
  features.unloading_country_code = mainItem ? extractCountryCode(mainItem.unloading_location) : null;

  // 11. TLD from domain
  features.tld = extractTld(scoresDoc.domain || scoresDoc.scored_domain);

  return features;
}

// ============================================================
// EXPORTS (for Node.js testing)
// ============================================================
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    predictConversionProbability: predictConversionProbability,
    computeMultiplier: computeMultiplier,
    calculateAdjustedValue: calculateAdjustedValue,
    getMonitoringLabel: getMonitoringLabel,
    getGadsLabel: getGadsLabel,
    buildFeatures: buildFeatures,
    parseNaceCodes: parseNaceCodes,
    extractTld: extractTld,
    extractLanguage: extractLanguage,
    extractCountryCode: extractCountryCode,
    toModelString: toModelString,
    NACE_DIVISION_TO_SECTION: NACE_DIVISION_TO_SECTION,
    VEHICLE_TYPE_MAP: VEHICLE_TYPE_MAP,
    TRANSPORT_TYPE_MAP: TRANSPORT_TYPE_MAP,
    NUMERIC_FEATURES: NUMERIC_FEATURES,
    CATEGORICAL_WEIGHTS: CATEGORICAL_WEIGHTS,
    INTERCEPT: INTERCEPT
  };
}
