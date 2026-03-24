---
name: Add logToConsole debug logging to sGTM templates immediately
description: Don't try to diagnose sGTM issues by guessing — add console logs from the start
type: feedback
---

When debugging sGTM custom templates, add `logToConsole()` at every decision point BEFORE guessing at the cause. Log variable values AND their types.

**Why:** During DATA-375, we wasted time speculating about why variables returned null (wrong Firestore data? missing cookie? wrong user_id?). The actual causes were: (1) variable not evaluated because nothing referenced it, (2) boolean vs string type mismatch, (3) Math.exp not available. All would have been immediately visible with logging.

**How to apply:**
1. Log inputs with types: `logToConsole('[TAG] input=' + val + ' (type: ' + getType(val) + ')')`
2. Log each gate/condition result before returning null
3. Log Firestore read results
4. Log the final computed value
5. Keep logs in production (user preference) — they only show in Preview mode and have no performance impact
