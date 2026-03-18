---
name: JIRA DATA board workflow transitions
description: Transition IDs for moving tickets through the DATA board workflow statuses
type: reference
---

DATA board workflow transitions (team-managed):

| From | Transition ID | To |
|------|--------------|-----|
| To Do | 6 | In Progress |
| To Do | 9 | BLOCKED |
| In Progress | 7 | Review |
| In Progress | 10 | BLOCKED |
| In Progress | 13 | To Do |

Sprint field: `customfield_10020` (expects integer sprint ID, not object).

To get active sprint: `GET /rest/agile/1.0/board/19/sprint?state=active`
