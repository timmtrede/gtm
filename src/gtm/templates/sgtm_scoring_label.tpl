___INFO___

{
  "type": "MACRO",
  "id": "cvt_scoring_label",
  "version": 1,
  "securityGroups": [],
  "displayName": "Scoring - Label",
  "description": "Returns customer segment label based on conversion probability: b_kunden / a_kunden / a_plus_kunden. Returns null if probability is null.",
  "containerContexts": [
    "SERVER"
  ]
}


___TEMPLATE_PARAMETERS___

[
  {
    "type": "TEXT",
    "name": "probability",
    "displayName": "Conversion Probability",
    "simpleValueType": true,
    "help": "The scoring.conversion_probability variable. Set to {{scoring.conversion_probability}}."
  }
]


___SANDBOXED_JS_FOR_SERVER___

const makeNumber = require('makeNumber');
const getType = require('getType');

const prob = data.probability;

// Return null if probability is not available
if (prob == null || prob === '' || prob === 'null' || prob === 'undefined') {
  return null;
}

const p = makeNumber(prob);
if (getType(p) !== 'number') {
  return null;
}

// clamp(prob * 3, 0.6, 2.4) then bucket
let multiplier = p * 3;
if (multiplier > 2.4) multiplier = 2.4;
if (multiplier < 0.6) multiplier = 0.6;

if (multiplier < 0.8) return 'b_kunden';
if (multiplier < 1.2 + 0.000000001) return 'a_kunden';  // float tolerance for 0.4*3=1.2
return 'a_plus_kunden';


___TESTS___

// See test_scoring_model_v4.js for Node.js tests


___NOTES___

Buckets (based on multiplier = clamp(prob * 3, 0.6, 2.4)):
  < 0.8     -> b_kunden    (B-Kunden)
  [0.8,1.2] -> a_kunden    (A-Kunden)
  > 1.2     -> a_plus_kunden (A+ Kunden)

Google Ads label mapping (done in alookup.gads_variable_label):
  b_kunden       -> kIETCImEtuYaEObk9sED
  a_kunden       -> 5PHlCJX_qOYaEObk9sED
  a_plus_kunden  -> 2JWlCIOsqIwcEObk9sED

JIRA: DATA-375
