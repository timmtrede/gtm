---
name: Spec-first workflow with inline Q&A
description: Start feature work with a spec in specs/, include open questions, and let the user answer directly in the file before implementation
type: feedback
---

For non-trivial features, always start with a spec file in `specs/` before writing any code.

**Why:** Aligns expectations early, surfaces edge cases via open questions, and creates a reference document for the implementation. The user answers questions directly in the spec file (inline below the question rows) — watch for file modifications.

**How to apply:**
1. Write the spec with overview, requirements, architecture, testing plan, and open questions
2. Mark status as "Draft — Open Questions Pending"
3. Wait for the user to answer questions (they edit the file directly)
4. Update the spec with resolved answers, change status to "Ready for Implementation"
5. Use the spec as the source of truth during implementation
