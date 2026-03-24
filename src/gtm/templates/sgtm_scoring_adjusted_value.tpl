___INFO___

{
  "type": "MACRO",
  "id": "cvt_scoring_adjusted_value",
  "version": 1,
  "securityGroups": [],
  "displayName": "Scoring - Adjusted Value",
  "description": "Computes adjusted conversion value: clamp(probability * 3, 0.6, 2.4) * revenue. Returns null if probability is null.",
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
  },
  {
    "type": "TEXT",
    "name": "revenue",
    "displayName": "Revenue (EUR)",
    "simpleValueType": true,
    "help": "The transaction value in EUR. Set to {{ed.value_eur}} or {{ed.value}}."
  }
]


___SANDBOXED_JS_FOR_SERVER___

const makeNumber = require('makeNumber');
const Math = require('Math');
const getType = require('getType');

const prob = data.probability;
const revenue = data.revenue;

// Return null if probability is not available (non-first, generic, error)
if (prob == null || prob === '' || prob === 'null' || prob === 'undefined') {
  return null;
}

const p = makeNumber(prob);
const r = makeNumber(revenue);

if (getType(p) !== 'number' || getType(r) !== 'number' || r === 0) {
  return null;
}

// clamp(prob * 3, 0.6, 2.4)
let multiplier = p * 3;
if (multiplier > 2.4) multiplier = 2.4;
if (multiplier < 0.6) multiplier = 0.6;

// Round to 2 decimal places
return Math.round(multiplier * r * 100) / 100;


___TESTS___

// See test_scoring_model_v4.js for Node.js tests


___NOTES___

Formula: clamp(probability * 3, 0.6, 2.4) * revenue
Input: scoring.conversion_probability + ed.value_eur (or ed.value)
Output: adjusted conversion value in EUR, or null
JIRA: DATA-375
