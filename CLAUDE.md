# CLAUDE.md

## Project Overview

This is a **GTM-as-Code** repository for managing the **Zipmend** Google Tag Manager account via Python CLI and MCP server. It provides programmatic CRUD operations, auditing, versioning, and backup capabilities for GTM containers.

GCP project: `zipmend-2e643`. GTM Account ID: `6002017930`.

## GTM Account Details

- **Account ID**: 6002017930
- **Auth**: Application Default Credentials (ADC) with GTM scopes
- **API**: Tag Manager API v2

## Architecture

```
src/gtm/
├── client.py          # GTM API client wrapper (ADC auth, retry)
├── models.py          # Pydantic models for all GTM resources
├── operations/        # One module per resource type
│   ├── containers.py  # List, get, export
│   ├── tags.py        # CRUD + search
│   ├── triggers.py    # CRUD
│   ├── variables.py   # CRUD
│   ├── versions.py    # Create, publish, diff
│   ├── workspaces.py  # List, create, delete
│   └── audit.py       # Naming, unused, duplicate checks
├── cli.py             # Typer CLI (entry point: `gtm`)
├── mcp_server.py      # FastMCP server for Claude Code
└── utils/
    ├── diff.py        # JSON diff utilities
    └── export.py      # Container export helpers
```

## CLI Usage

```bash
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
```

## MCP Server

The MCP server (`src/gtm/mcp_server.py`) exposes all operations as tools. Registered in `.mcp.json`. Tools are annotated with `readOnlyHint` or `destructiveHint`.

## Auth Setup

ADC with GTM scopes:
```bash
gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/tagmanager.readonly,https://www.googleapis.com/auth/tagmanager.edit.containers,https://www.googleapis.com/auth/tagmanager.edit.containerversions,https://www.googleapis.com/auth/tagmanager.publish,https://www.googleapis.com/auth/cloud-platform
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
- `GITHUB_TOKEN` — for GitHub operations
- `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` — for DATA board tickets

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
