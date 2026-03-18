---
name: Always use PRs, never push directly to main
description: Never commit/push directly to main — always create a short, specific branch and open a PR
type: feedback
---

Never push directly to `main`. Always create a new branch and open a PR, even for small fixes.

**Why:** It's best practice to use pull requests for all changes — it provides a review checkpoint and keeps the history clean.

**How to apply:** When asked to commit and push, create a short, descriptive branch name (e.g., `fix/cloudtalk-syntax-error`), push to that branch, and create a PR via `gh pr create`.
