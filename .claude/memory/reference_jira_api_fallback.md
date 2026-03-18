---
name: JIRA API fallback via curl
description: When the Atlassian MCP integration fails, use curl with credentials from .env to access the JIRA REST API
type: reference
---

The Atlassian MCP integration can fail with auth errors. Fallback approach:

1. Read credentials from `.env` in project root:
   - `JIRA_BASE_URL`
   - `JIRA_EMAIL`
   - `JIRA_API_TOKEN`
2. Use curl with basic auth: `-u "$JIRA_EMAIL:$JIRA_API_TOKEN"`
3. Subtask issue type ID for DATA project: `10039`
4. Example: `curl -s -X POST -u "email:token" -H "Content-Type: application/json" "$JIRA_BASE_URL/rest/api/3/issue" -d '{"fields": {"project": {"key": "DATA"}, "parent": {"key": "DATA-NNN"}, "issuetype": {"id": "10039"}, "summary": "..."}}'`
