---
name: Always fetch remote before assuming local is current
description: User often commits/pushes from GitHub UI or IDE separately — local branch may be behind remote
type: feedback
---

Always `git fetch origin` before concluding a commit doesn't exist. The user frequently pushes commits from outside the CLI (e.g., GitHub UI, PyCharm), so the local branch can be behind `origin`.

**Why:** Wasted time looking for a commit locally that only existed on the remote, required the user to share the GitHub URL before I thought to fetch.

**How to apply:** When the user references a commit or says they made changes, fetch from remote first before inspecting local state.
