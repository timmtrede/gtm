---
name: All learnings must live in the repo
description: All Claude Code memories, skills, commands, and learnings must be committed to the .claude/ directory in the repo so they are available to anyone cloning it
type: feedback
---

Everything Claude Code learns — memories, skills, commands, templates — must be stored in the repo's `.claude/` directory and committed to git. The local `~/.claude/projects/` memory path is symlinked to the repo.

**Why:** Learnings should persist across users and machines. Anyone cloning the repo should get the full context without re-teaching Claude. This also provides version control for knowledge.

**How to apply:**
1. The symlink `~/.claude/projects/-Users-jeremie-PycharmProjects-gtm/memory` → `/Users/jeremie/PycharmProjects/gtm/.claude/memory` is set up — writes go directly to the repo
2. After creating or updating any memory, skill, command, or template in `.claude/`, include the changes in the next git commit
3. New users cloning the repo should create the same symlink to activate the memories locally
