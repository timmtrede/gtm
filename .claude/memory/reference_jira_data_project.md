---
name: JIRA DATA project setup
description: JIRA configuration for the DATA board — project key, board ID, issue types, and field details
type: reference
---

JIRA project for data/analytics work:
- **Project key**: DATA (id: 10021)
- **Board**: 19 (DATA board, simple/kanban)
- **Style**: Team-managed (next-gen) — simpler field set than company-managed ZIP
- **Credentials**: `.env` file at project root (JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN)
- **Base URL**: https://zipmend.atlassian.net

Issue types:
| Type | ID |
|------|-----|
| Task | 10037 |
| Epic | 10038 |
| Subtask | 10039 |
| Story | 10440 |
| Bug | 10441 |

Available fields (all types): summary, description, assignee, reporter, labels, fixVersions, duedate, parent, sprint (customfield_10020), flagged (customfield_10021), issuelinks.

No custom bug fields (Steps to Reproduce, etc.) — everything goes in the ADF description.
