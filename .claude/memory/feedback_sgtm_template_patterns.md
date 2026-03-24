---
name: sGTM template development patterns
description: Hard-won lessons from building sGTM custom variable templates — sandboxed JS limitations, async behavior, null handling
type: feedback
---

Key sGTM sandboxed JS constraints discovered during DATA-375:

1. **No `Math.exp()`** — use repeated squaring approximation: `ex = (1 + x/65536)^65536` (16 iterations) for ~6 decimal place accuracy.
2. **No scientific notation in literals** — `1.107e-5` causes parse error. Write `0.00001107` instead.
3. **Variables are lazily evaluated** — only computed when referenced by a tag/trigger that actually fires. A variable that exists but isn't referenced by anything will show null in Preview.
4. **Async variables (Firestore.read) need trigger gating** — if a tag depends on an async variable, the trigger must include a condition on that variable (or a downstream variable) to force sGTM to resolve it before the trigger evaluates.
5. **Firestore returns booleans as actual booleans** (`true`/`false`), not strings (`"true"`/`"false"`). Templates must handle both: `if (val === true || val === 'true')`.
6. **Advanced Lookup Table (`cvt_*_22`) cannot reliably detect null** — `doesNotEqual "undefined"` fires for both valid values AND null. Use `equals` on known string values instead.
7. **`convertNullToValue: "false"` returns boolean `false`**, not string `"false"`. This broke a string comparison gate initially.

**Why:** These all caused bugs during implementation that required debugging cycles.

**How to apply:** When building sGTM templates, always: (a) test with `logToConsole` at every decision point, (b) verify types with `getType()`, (c) avoid `doesNotEqual` for null detection, (d) check Math API availability early.
