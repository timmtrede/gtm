___INFO___

{
  "type": "MACRO",
  "id": "cvt_scoring_conversion_probability",
  "version": 1,
  "securityGroups": [],
  "displayName": "Scoring - Conversion Probability",
  "description": "Predicts 3+ order probability for a domain using company_scoring_v4 logistic regression. Returns probability (0-1) for non-generic first orders with a scores doc, null otherwise.",
  "containerContexts": [
    "SERVER"
  ]
}


___TEMPLATE_PARAMETERS___

[]


___SANDBOXED_JS_FOR_SERVER___

// sGTM Template: scoring.conversion_probability
// Model: zipmend-2e643.ml.company_scoring_v4
// JIRA: DATA-375

const getEventData = require('getEventData');
const Firestore = require('Firestore');
const JSON = require('JSON');
const Math = require('Math');
const getType = require('getType');
const makeString = require('makeString');
const makeNumber = require('makeNumber');
const logToConsole = require('logToConsole');

// ============================================================
// NACE DIVISION-TO-SECTION MAPPING
// ============================================================
const NACE_MAP = {
  1:"a",2:"a",3:"a",5:"b",6:"b",7:"b",8:"b",9:"b",
  10:"c",11:"c",12:"c",13:"c",14:"c",15:"c",16:"c",17:"c",18:"c",19:"c",
  20:"c",21:"c",22:"c",23:"c",24:"c",25:"c",26:"c",27:"c",28:"c",29:"c",
  30:"c",31:"c",32:"c",33:"c",35:"d",36:"e",37:"e",38:"e",39:"e",
  41:"f",42:"f",43:"f",45:"g",46:"g",47:"g",49:"h",50:"h",51:"h",52:"h",53:"h",
  55:"i",56:"i",58:"j",59:"j",60:"j",61:"j",62:"j",63:"j",64:"k",65:"k",66:"k",
  68:"l",69:"m",70:"m",71:"m",72:"m",73:"m",74:"m",75:"m",77:"n",78:"n",79:"n",
  80:"n",81:"n",82:"n",84:"o",85:"p",86:"q",87:"q",88:"q",90:"r",91:"r",92:"r",
  93:"r",94:"s",95:"s",96:"s",97:"t",98:"t",99:"u"
};

// ============================================================
// VEHICLE TYPE MAPPING (item_id string -> model key)
// ============================================================
const VT_MAP = {
  "0":"Large van","1":"Tail lift and pallet truck",
  "2":"Length 450cm loading space","3":"Length 480cm loading space",
  "4":"Width 220cm loading space","5":"Width 230cm loading space",
  "7":"Large van","8":"Loading from above","9":"Dangerous Goods",
  "10":"Large van","11":"Small van","12":"Medium van",
  "13":"24t Shipment","14":"2,4t Shipment","15":"5t Shipment",
  "16":"12t Shipment","17":"3,2t Shipment"
};

// ============================================================
// MODEL WEIGHTS
// ============================================================
const INTERCEPT = 0.19609285288872272;

const NUM = {
  net_revenue_first_transport:{w:0.00001107061766784912,m:366.1414280793821,s:321.82600082883715},
  distance_first_transport:{w:0.00006323441850322997,m:316.16649780479764,s:320.1420009659045},
  a:{w:-0.3724418399822121,m:0.007880220646178123,s:0.08842512646147806},
  b:{w:-0.06417412913497608,m:0.0020263424518743647,s:0.044971814130477954},
  c:{w:-0.2632725211672573,m:0.2289766970618035,s:0.4201978654581521},
  d:{w:-0.49517150148598943,m:0.006304176516942455,s:0.07915263211543014},
  e:{w:-0.3233593619270897,m:0.010919734323989686,s:0.1039312740431183},
  f:{w:-0.31192458934273726,m:0.08656985252729928,s:0.2812195157802441},
  g:{w:-0.33773296920594353,m:0.11910390633794907,s:0.3239289710434889},
  h:{w:-0.1137643669608994,m:0.03320950129460761,s:0.179193317720695},
  i:{w:-0.3504966677499206,m:0.01531014296971746,s:0.12279022692555953},
  j:{w:-0.2760497540103016,m:0.020038275357424258,s:0.14013905139219598},
  k:{w:-0.26846351745026564,m:0.06022740065293277,s:0.2379210652906047},
  l:{w:-0.42024230124900225,m:0.01114488348530901,s:0.10498531252019136},
  m:{w:-0.4108003711413672,m:0.01564786671169644,s:0.12411585378909575},
  n:{w:-0.298967049218506,m:0.1794438815715416,s:0.38374516636764844},
  o:{w:-0.23946870367145703,m:0.05516154452324664,s:0.22830816112415636},
  p:{w:-0.44168843033004374,m:0.002701789935832494,s:0.051911401755666726},
  q:{w:-0.31568583174643416,m:0.022965214454576104,s:0.1498009999681272},
  r:{w:-0.32659569463848465,m:0.015422717550377125,s:0.1232337898270804},
  s:{w:-0.39376798196052365,m:0.01879995497016775,s:0.13582559959729631},
  t:{w:-0.34740888783379653,m:0.016661037937633627,s:0.12800504802501472},
  u:{w:-0.4716439511463671,m:0.00011257458065968654,s:0.01061011690132048}
};

const CAT = {
  no_shipping_required:{"false":0.023170144583303243,"true":-0.2100050877451799,"unknown":-0.21668976294307804,_null:0},
  b2b_business_model:{"false":-0.12742904380817627,"true":-0.03191401420500469,"unknown":-0.09014046223464109,_null:0},
  logistics_transportation:{"false":-0.09141360555907964,"true":0.15029359800121406,"unknown":-0.056748765001659054,_null:0},
  min_200_employees:{"false":-0.20322449080190091,"true":-0.005473507280983768,"unknown":0.01228560443283689,_null:0},
  non_eu_operations:{"false":-0.05086572354888771,"true":-0.17450094987563347,"unknown":0.004903253255952854,_null:0},
  turnover_10m_to_500m_eur:{"false":-0.16150812880266724,"true":-0.09645440891765765,"unknown":-0.0449481513979897,_null:0},
  heavy_large_products:{"false":-0.050820388714084494,"true":-0.062310795252904845,"unknown":0.025326354673188205,_null:0},
  operates_europe_wide:{"false":-0.1812178769217589,"true":0.03169008753973013,"unknown":-0.05772174798582227,_null:0},
  manufactures_product:{"false":-0.09135988284829209,"true":-0.01578573170173398,"unknown":-0.28816673660538455,_null:0},
  mainly_b2c:{"false":-0.030404572212813043,"true":-0.11933925103442233,"unknown":-0.09323862402918759,_null:0},
  high_quality_physical_goods:{"false":-0.08407194863374717,"true":-0.024769104380562765,"unknown":-0.1443110899430542,_null:0},
  low_cost_consumer_products:{"false":-0.05565687419125419,"true":0.05026151070673836,"unknown":-0.2820964795098649,"partial":-0.7191522565129611,_null:0},
  online:{"true":-0.07541606842202789,"false":-0.5397222798605793,_null:0.1062734370313775},
  payment_method:{"invoice":-0.00000593473779407494,"creditcard":-0.16222340897896984,"paypal":0.035444836044058126,"klarna":-0.4204481799079659,"bancontact":0.32839560966525144,"ideal":-0.1318001141983648,"sofort":-0.4204481799079659,"advance_payment":0.041069443765247904,"advance_payment_wise":0.041069443765247904,"advancepayment":0.041069443765247904,"przelewy24":-0.35585390151964036,"belfius":-0.8998594267255149,"billie":0.046636753465026104,"trustly":0,_null:-0.35117487703131195},
  transport_type_first_transport:{"express_1200_kg":-0.07164918243729212,"full_truck_24_t":0.07856094735676566,_null:0.7314563562221194},
  vehicle_type_first_transport:{"loading from above":-1.0090647288605212,"overhang":-0.7455498019249021,"small van":-0.14500307813606342,"tail lift and pallet truck":-0.14619399492007565,"3,2t shipment":-0.01934229068327046,"dangerous goods":0.009642811761652511,"12t shipment":0.018337507885265166,"medium van":0.0459485798505546,"width 230cm loading space":0.19575835527804575,"2,4t shipment":0.19739518683690896,"24t shipment":0.18550335110407606,"width 220cm loading space":0.20939917092622387,"large van":0.2721545098397925,"5t shipment":0.2785774636546063,"length 480cm loading space":0.710275693059552,"length 450cm loading space":0.9796427358149071,"cooling-vehicle":1.5447771209066998,_null:0.7314563562221194},
  shipper_language:{"cs":-0.2364902016064497,"da":-0.3346683179634214,"de":0.012438440538666032,"en":0.13408050154306417,"es":-0.3452472562353442,"fr":-0.18428981718833637,"it":-0.06614715935468193,"nl":-0.01332541076048741,"pl":-0.20107492818628617,_null:0.9685348059675722},
  loading_country_code:{"at":0.052630829955904554,"be":0.05735337090407901,"bg":0.33480260239603316,"ch":-0.3574806137560447,"cz":-0.3173167981151924,"de":0.04981692174870813,"dk":-0.05756833928405996,"ee":1.6664561937426199,"es":-0.2550982808619707,"fi":-1.1370994096132252,"fr":-0.19737740227039333,"gb":-0.20068450228647428,"hr":-0.9488181600180816,"hu":1.7494432048512736,"it":-0.002189422835830118,"lu":0.15605535818398883,"mc":-0.6497010563227194,"nl":-0.012654741663777988,"pl":-0.17030881838838308,"pt":-0.12912270582442836,"ro":1.6041755370842918,"se":0.13368900971362854,"si":-0.9384967242965124,"sk":1.0830929558070248,_null:0},
  unloading_country_code:{"at":-0.0317014617214245,"be":0.05983985331793877,"bg":-0.8486482795862077,"ch":-0.3767013435373036,"cz":0.006202220511354719,"de":0.026212912128504465,"dk":0.11522243470303177,"es":-0.23908724267652284,"fr":-0.1794292913251229,"gb":-0.20158088851896402,"hr":0.3365195383612399,"hu":0.7561582222746955,"it":0.03336274722484016,"lt":0.6462978594512653,"lu":0.0014041763048870046,"lv":-0.9061673375654165,"mc":-0.8012708854025692,"nl":-0.004952206699566343,"pl":0.019005906981966757,"pt":-0.3127772784489193,"se":0.44609934458403266,"si":-0.21833161998479186,"sk":0.2652945915113065,_null:0},
  tld:{".aero":0.6502634152327026,".ag":0.43231921896807124,".agency":-0.43272025552234,".ai":-0.003480242253640681,".amsterdam":1.6635411026530031,".app":-0.9066106295913593,".ar":-0.7750471250959377,".archi":-0.5841714708057819,".art":0.2000578279429108,".at":0.011254480084047003,".be":0.0863372067517017,".beer":-0.7506684779687889,".berlin":-0.7378980550621429,".bg":-0.5909244364668889,".bike":2.010964308814818,".bio":0.1405543398750746,".biz":0.4677183633269249,".business":-0.6692947386942757,".ca":0.6907320111323177,".care":-0.9028522846729727,".cat":-0.6400932794130567,".cc":-0.2565745110372459,".ch":-0.5283264692305081,".cloud":0.3962096117023705,".club":-0.6893749533343131,".cn":-0.0009229268777407734,".co":0.20431015931105817,".com":-0.010379525113181135,".company":-1.0451816899599393,".coop":-0.6194922106044662,".cy":-1.0522807626814823,".cz":0.0943210264503995,".de":-0.014812343825890235,".dev":-0.6860838411964041,".digital":0.2833177654410286,".dk":-0.1794531384982014,".earth":-0.864697217848788,".edu":-0.7194896096787968,".education":2.236703617326663,".energy":-0.7540372823712933,".es":-0.4074533293966866,".eu":-0.0755346080155647,".events":1.9654708366935727,".expert":-0.7001807355738416,".financial":-0.6887683089338323,".fr":-0.18171200489019243,".games":-0.7432109768312829,".gg":0.7445236290687979,".global":-0.335049632708224,".gmbh":-0.38840974652938426,".group":-0.09525267945323382,".gy":2.080688866267988,".hamburg":-1.1426608439385233,".health":2.266421770939927,".healthcare":-0.8013911108872812,".hk":2.116574893875189,".house":0.3902667121450253,".hr":-1.102905004603688,".hu":-0.9873772697158445,".ie":-0.6956249677120364,".il":-0.8360650644053133,".immo":-0.6952253656488734,".immobilien":-0.8849425235548725,".inc":-0.8739548579564496,".info":-0.20881474904244846,".international":-0.950013394481779,".io":-0.1035509052565893,".it":-0.1700182247197127,".jp":-1.1067170123396066,".kids":-0.7874451645001229,".koeln":0.1503178082798481,".kr":-0.8424260420274503,".la":-0.8751055197428415,".land":2.2174524996750318,".law":1.1351007681882985,".leclerc":-0.7168124104430251,".legal":-0.8169801115155572,".life":1.1023738613580099,".lt":-0.9141002834515117,".lu":0.11793852900880152,".me":0.3604704572123422,".media":-0.8855566576466536,".moe":-0.6606828879703097,".ms":-1.0032318088061456,".mt":-0.9149326628033754,".mu":-0.6386508662976813,".museum":-0.9810860397477745,".net":0.015709660000029952,".network":-0.9633327887837395,".nl":-0.09335686965367644,".nrw":-0.852337666485662,".nu":2.200693569777098,".one":-0.9889606992959515,".online":0.4673468705537943,".org":-0.2113019316642931,".ovh":2.190815711655396,".paris":-0.08475658204024497,".pl":-0.19167977843929904,".plus":1.7319733799317678,".pro":0.12391740234793644,".productions":1.8290781870735,".pt":-0.6882743760141289,".re":-0.7577952550138694,".ro":-0.7782520757696013,".rocks":1.9244633348698574,".schule":-0.9657027394181049,".se":-0.8600003156429166,".sener":-0.9466059998572675,".services":1.6628783927922006,".sg":-1.2047762744610424,".shop":-0.6509377675601441,".site":1.7888001856603253,".sk":-0.9561200261167013,".so":-0.7410934618240594,".solutions":0.7827854883731726,".space":-0.8072676611248851,".store":-0.3112813482352293,".studio":-0.1460479496218846,".support":1.851647914313975,".systems":1.7958456954592816,".tax":0.612356903477952,".team":-0.6962709620072306,".tech":0.14310246195216092,".tirol":0.14109729788592063,".tr":-0.9818934915094663,".tv":-0.513953133495216,".uk":-0.33012300882324114,".us":-0.8929793032651698,".vin":-0.7668210829912783,".vision":-0.698272438322039,".work":-0.7053453806108098,".world":1.7042873397678695,".xyz":-0.6027411024499743,_null:0}
};

// ============================================================
// HELPER: convert Firestore bool/string to lowercase model string
// ============================================================
function toStr(val) {
  if (val === true) return "true";
  if (val === false) return "false";
  if (getType(val) === 'string') return val.toLowerCase();
  return null;
}

// ============================================================
// HELPER: parse NACE codes JSON string to one-hot object
// ============================================================
function parseNace(naceStr) {
  const letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u"];
  const result = {};
  for (let i = 0; i < letters.length; i++) result[letters[i]] = 0;
  if (!naceStr) return result;
  const codes = JSON.parse(naceStr);
  if (!codes || getType(codes) !== 'array') return result;
  for (let j = 0; j < codes.length; j++) {
    const div = Math.floor(makeNumber(codes[j]));
    if (NACE_MAP[div]) result[NACE_MAP[div]] = 1;
  }
  return result;
}

// ============================================================
// HELPER: extract TLD from domain
// ============================================================
function getTld(domain) {
  if (!domain) return null;
  const idx = domain.lastIndexOf('.');
  return idx >= 0 ? domain.substring(idx).toLowerCase() : null;
}

// ============================================================
// HELPER: extract language from page_path /v2/{lang}/...
// ============================================================
function getLang(pagePath) {
  if (!pagePath) return null;
  const parts = pagePath.split('/');
  // parts: ["", "v2", "de", "booking", ...]
  if (parts.length >= 3 && parts[1] === 'v2' && parts[2].length === 2) {
    return parts[2].toLowerCase();
  }
  return null;
}

// ============================================================
// HELPER: find main_products item from items array
// ============================================================
function findMainItem(items) {
  if (!items || getType(items) !== 'array') return null;
  for (let i = 0; i < items.length; i++) {
    const iln = items[i].item_list_name;
    if (iln && makeString(iln).indexOf('main_products') >= 0) {
      return items[i];
    }
  }
  return null;
}

// ============================================================
// MAIN: run prediction
// ============================================================

const firstOrder = data.firstOrder;
const isGeneric = data.isGeneric;
const domain = data.domain;

logToConsole('[SCORING] === START ===');
logToConsole('[SCORING] firstOrder=' + firstOrder + ' (type: ' + getType(firstOrder) + ')');
logToConsole('[SCORING] isGeneric=' + isGeneric + ' (type: ' + getType(isGeneric) + ')');
logToConsole('[SCORING] domain=' + domain + ' (type: ' + getType(domain) + ')');

// Gate: only score non-generic first orders
if (firstOrder !== 'true') {
  logToConsole('[SCORING] GATE FAILED: firstOrder !== "true"');
  return null;
}
if (isGeneric !== 'false' && isGeneric !== false) {
  logToConsole('[SCORING] GATE FAILED: isGeneric is not false (got: ' + isGeneric + ', type: ' + getType(isGeneric) + ')');
  return null;
}
if (!domain) {
  logToConsole('[SCORING] GATE FAILED: domain is falsy');
  return null;
}
logToConsole('[SCORING] Gate passed, reading Firestore scores/' + domain);

// Read Firestore scores document
const projectId = 'zipmend-2e643';
return Firestore.read('scores/' + domain, { projectId: projectId })
  .then(function(doc) {
    logToConsole('[SCORING] Firestore response: doc=' + (doc ? 'exists' : 'null') + ', doc.data=' + (doc && doc.data ? 'exists' : 'null'));
    if (!doc || !doc.data) {
      logToConsole('[SCORING] No scores document for domain: ' + domain);
      return null;
    }
    const sd = doc.data;
    logToConsole('[SCORING] Scores doc fields: domain=' + sd.domain + ', score=' + sd.score + ', nace_codes=' + sd.nace_codes);

    // Gather event data
    const valueEur = getEventData('value_eur') || getEventData('value');
    const pagePath = getEventData('page_path');
    const paymentType = getEventData('payment_type');
    const orderOrigin = getEventData('order_origin');
    const items = getEventData('items');
    const mainItem = findMainItem(items);

    logToConsole('[SCORING] Event: valueEur=' + valueEur + ', pagePath=' + pagePath + ', paymentType=' + paymentType + ', orderOrigin=' + orderOrigin);
    logToConsole('[SCORING] Items: ' + (items ? ('array len=' + items.length) : 'null') + ', mainItem=' + (mainItem ? ('id=' + mainItem.item_id + ' cat=' + mainItem.item_category) : 'null'));

    // Build features
    const features = {};

    // Company profile
    const profileFields = [
      'no_shipping_required','b2b_business_model','logistics_transportation',
      'min_200_employees','non_eu_operations','turnover_10m_to_500m_eur',
      'heavy_large_products','operates_europe_wide','manufactures_product',
      'mainly_b2c','high_quality_physical_goods','low_cost_consumer_products'
    ];
    for (let i = 0; i < profileFields.length; i++) {
      features[profileFields[i]] = toStr(sd[profileFields[i]]);
    }

    // NACE one-hot
    const nace = parseNace(sd.nace_codes);
    for (const letter in nace) features[letter] = nace[letter];

    // Revenue
    features.net_revenue_first_transport = makeNumber(valueEur) || null;

    // Items data
    if (mainItem) {
      features.distance_first_transport = makeNumber(mainItem.distance) || null;
      const cat = mainItem.item_category;
      features.transport_type_first_transport = cat ? (cat.toLowerCase() === 'express' ? 'express_1200_kg' : (cat.toLowerCase() === 'lkw' ? 'full_truck_24_t' : null)) : null;
      const vid = makeString(mainItem.item_id);
      features.vehicle_type_first_transport = VT_MAP[vid] || null;
      const ll = mainItem.loading_location;
      features.loading_country_code = (ll && makeString(ll).length >= 2) ? makeString(ll).substring(0, 2).toLowerCase() : null;
      const ul = mainItem.unloading_location;
      features.unloading_country_code = (ul && makeString(ul).length >= 2) ? makeString(ul).substring(0, 2).toLowerCase() : null;
    }

    // Event-level features
    features.online = orderOrigin === 'online' ? 'true' : (orderOrigin ? 'false' : null);
    features.payment_method = paymentType ? paymentType.toLowerCase() : null;
    features.shipper_language = getLang(pagePath);
    features.tld = getTld(sd.domain || sd.scored_domain || domain);

    logToConsole('[SCORING] Features built: tld=' + features.tld + ', lang=' + features.shipper_language + ', payment=' + features.payment_method + ', vehicle=' + features.vehicle_type_first_transport + ', transport=' + features.transport_type_first_transport + ', online=' + features.online);
    logToConsole('[SCORING] Revenue=' + features.net_revenue_first_transport + ', distance=' + features.distance_first_transport + ', load=' + features.loading_country_code + ', unload=' + features.unloading_country_code);

    // Run logistic regression
    let z = INTERCEPT;

    // Numeric features
    for (const nk in NUM) {
      const nf = NUM[nk];
      const nv = features[nk] != null ? features[nk] : nf.m;
      if (nf.s > 0) z += nf.w * (nv - nf.m) / nf.s;
    }

    // Categorical features
    for (const ck in CAT) {
      const cv = features[ck] != null ? makeString(features[ck]).toLowerCase() : null;
      const cw = CAT[ck];
      if (cv === null || cv === 'null') {
        z += cw._null || 0;
      } else if (cw[cv] != null) {
        z += cw[cv];
      }
    }

    // Sigmoid (Math.exp not available in sGTM sandbox)
    // exp(x) via repeated squaring: exp(x) = (1 + x/65536)^65536
    const zc = z < -20 ? -20 : (z > 20 ? 20 : z);
    let ex = 1 + (-zc) / 65536;
    for (let step = 0; step < 16; step++) { ex = ex * ex; }
    const prob = 1 / (1 + ex);
    logToConsole('[SCORING] z_score=' + z + ', probability=' + prob);
    logToConsole('[SCORING] === DONE ===');
    return prob;
  })
  .catch(function(err) {
    logToConsole('[SCORING] ERROR: ' + err);
    return null;
  });


___TESTS___

// No built-in sGTM template tests — see test_scoring_model_v4.js for Node.js tests


___NOTES___

Model: company_scoring_v4 (logistic regression)
Predicts: probability of domain placing 3+ orders
Scope: non-generic first orders with Firestore scores document only
Fallback: returns null (downstream falls back to ed.value)
JIRA: DATA-375
