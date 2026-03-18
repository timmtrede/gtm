# CLAUDE.md

## Project Overview

This is a **GTM-as-Code** repository for managing the **Zipmend** Google Tag Manager account via Python CLI and MCP server. It provides programmatic CRUD operations, auditing, versioning, and backup capabilities for GTM containers, plus read-only access to **Firestore** and **BigQuery** data produced by the GTM server container.

GCP project: `zipmend-2e643`. GTM Account ID: `6002017930`.

## GOLDEN RULE

**Never write, update, or delete data in Firestore or BigQuery without explicit double confirmation from the user.** All Firestore and BigQuery operations must be read-only unless the user confirms twice.

## GTM Account Details

- **Account ID**: 6002017930
- **Auth**: Service account (`claude-gtm-manager@zipmend-2e643.iam.gserviceaccount.com`)
- **API**: Tag Manager API v2
- **IAM Roles**: `roles/datastore.user`, `roles/bigquery.dataViewer`, `roles/bigquery.jobUser`

## Architecture

```
src/gtm/
├── client.py              # GTM API client wrapper (service account auth, retry)
├── firestore_client.py    # Firestore client wrapper
├── bigquery_client.py     # BigQuery client wrapper
├── models.py              # Pydantic models for all GTM resources
├── operations/            # One module per resource type
│   ├── containers.py      # List, get, export
│   ├── tags.py            # CRUD + search
│   ├── triggers.py        # CRUD
│   ├── variables.py       # CRUD
│   ├── versions.py        # Create, publish, diff
│   ├── workspaces.py      # List, create, delete
│   ├── audit.py           # Naming, unused, duplicate checks
│   ├── firestore_ops.py   # Firestore queries (events, customers, scores, domains)
│   └── bigquery_ops.py    # BigQuery queries (datasets, tables, schemas, SQL)
├── cli.py                 # Typer CLI (entry point: `gtm`)
├── mcp_server.py          # FastMCP server for Claude Code
└── utils/
    ├── diff.py            # JSON diff utilities
    └── export.py          # Container export helpers
```

## CLI Usage

```bash
# GTM Container Management
gtm containers list
gtm containers export <id>
gtm tags list --container <id>
gtm tags search "query" --container <id>
gtm triggers list --container <id>
gtm variables list --container <id>
gtm versions list --container <id>
gtm versions diff <v1> <v2> --container <id>
gtm audit --container <id>
gtm backup --container <id>

# Firestore (read-only)
gtm firestore collections
gtm firestore events --event <name> --user <id> --txn <id>
gtm firestore event <doc_id>
gtm firestore customers --user <id>
gtm firestore score <domain>
gtm firestore scores
gtm firestore domains --check <domain>
gtm firestore query <collection> --field <f> --value <v>

# BigQuery (read-only)
gtm bq datasets
gtm bq tables <dataset>
gtm bq schema <dataset> <table>
gtm bq preview <dataset> <table>
gtm bq query "<sql>"
gtm bq query --dry-run "<sql>"
```

## MCP Server

The MCP server (`src/gtm/mcp_server.py`) exposes all operations as tools. Registered in `.mcp.json`. Tools are annotated with `readOnlyHint` or `destructiveHint`.

## Agents

| Agent | Purpose |
|---|---|
| `gtm-auditor` | Audit containers for quality, compliance, best practices |
| `gtm-engineer` | CRUD operations on tags, triggers, variables |
| `gtm-explorer` | Explore container configurations |
| `gtm-jira` | Create JIRA tickets on DATA board |
| `gtm-versioner` | Version management (create, publish, diff, rollback) |
| `spec-writer` | Write technical specifications |
| `bq-analyst` | Query BigQuery, explore GA4 schemas, run analytics |
| `firestore-explorer` | Browse Firestore collections, query events/customers/scores |
| `data-validator` | Cross-reference GTM config against actual BQ/Firestore data |
| `sgtm-template-manager` | Inspect sGTM custom templates |

## Slash Commands

| Command | Agent | Description |
|---|---|---|
| `/gtm-audit` | gtm-auditor | Audit a container |
| `/gtm-backup` | gtm-versioner | Backup live version |
| `/gtm-dev` | gtm-engineer | Implement from a spec |
| `/gtm-explore` | gtm-explorer | Explore a container |
| `/gtm-jira` | gtm-jira | Create JIRA ticket |
| `/gtm-spec` | spec-writer | Write a spec |
| `/gtm-tag` | gtm-engineer | Manage tags |
| `/gtm-version` | gtm-versioner | Manage versions |
| `/bq-query` | bq-analyst | Run BigQuery SQL with cost estimate |
| `/bq-schema` | bq-analyst | Explore dataset/table schema |
| `/firestore-browse` | firestore-explorer | Browse a Firestore collection |
| `/firestore-stats` | firestore-explorer | Collection statistics |
| `/data-check` | data-validator | Validate tag data flow end-to-end |
| `/ga4-report` | bq-analyst | Run GA4 analytics reports |

## Reference Skills

| Skill | Content |
|---|---|
| `gtm-api` | GTM API v2 endpoints, auth, rate limits |
| `gtm-tags` | Tag types, parameters, consent mode |
| `gtm-audit` | Audit checklist |
| `gtm-versioning` | Version workflow, rollback, backup |
| `ga4-schema` | GA4 BigQuery export schema reference |
| `sgtm-firestore` | sGTM Firestore integration patterns |
| `bq-cost-guide` | BigQuery pricing, cost optimization |
| `ga4-sql-templates` | Reusable GA4 SQL queries |
| `mcp-builder` | FastMCP server building guide |
| `python-testing` | pytest patterns |

## Auth Setup

Service account credentials in `.credentials.json`:
```bash
# For GTM API + Firestore + BigQuery
# Service account: claude-gtm-manager@zipmend-2e643.iam.gserviceaccount.com
```

## Development

```bash
pip install -e ".[dev]"    # Install with dev dependencies
pytest                      # Run tests
ruff check src/             # Lint
```

## Naming Conventions

- Python modules: `snake_case`
- Pydantic models: `PascalCase`
- CLI commands: `kebab-case` subcommands under resource groups
- GTM resources: follow existing GTM container naming conventions

## Environment Variables

Set in `.env` (see `.env.example`):
- `GTM_ACCOUNT_ID` — GTM account ID (default: 6002017930)
- `GCP_PROJECT` — GCP project ID (default: zipmend-2e643)
- `GOOGLE_APPLICATION_CREDENTIALS` — path to service account key (default: .credentials.json)
- `GITHUB_TOKEN` — for GitHub operations
- `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` — for DATA board tickets

## Firestore Collections

| Collection | Docs | Purpose |
|---|---|---|
| `zipmend` | ~240k | GTM server container event data |
| `existing_customers` | ~68k | Customer user IDs |
| `scores` | ~23k | Company/lead scoring by domain |
| `generic_domains` | ~9k | Generic email domains |

## BigQuery Key Datasets

| Dataset | Content |
|---|---|
| `analytics_287815421` | GA4 raw event tables (daily sharded) |
| `superform_outputs_287815421` | Processed GA4 sessions, transactions |
| `DataWarehouse` | Business views (CLV, cohorts) |
| `dm_core` | Fact tables (orders, employees) |
| `reports` | Reporting tables |

## Claude Code Memory Setup

Project-specific learnings are stored in `.claude/memory/` and tracked in git.

**For new users cloning the repo**, activate memories:
```bash
ln -s /path/to/gtm/.claude/memory ~/.claude/projects/-path-to-gtm/memory
```

**Rules:**
- All learnings must live in the repo's `.claude/` directory
- Any new memory must be committed and pushed alongside code changes
- Never store learnings only in the local `~/.claude/` path
