# GTM-as-Code

Python CLI + MCP server for managing the Zipmend Google Tag Manager account programmatically.

## Setup

```bash
# Clone
git clone https://github.com/timmtrede/gtm.git
cd gtm

# Install
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env with your credentials

# Authenticate with GCP (GTM scopes)
gcloud auth application-default login \
  --scopes=openid,https://www.googleapis.com/auth/tagmanager.readonly,https://www.googleapis.com/auth/tagmanager.edit.containers,https://www.googleapis.com/auth/tagmanager.edit.containerversions,https://www.googleapis.com/auth/tagmanager.publish,https://www.googleapis.com/auth/cloud-platform
```

## Usage

```bash
gtm containers list
gtm tags list --container <id>
gtm audit --container <id>
gtm backup --container <id>
gtm versions diff <v1> <v2> --container <id>
```

## Claude Code Setup

Activate project memories:
```bash
ln -s $(pwd)/.claude/memory ~/.claude/projects/-$(pwd | tr '/' '-' | cut -c2-)/memory
```

## Architecture

```
src/gtm/
├── client.py          # GTM API v2 wrapper
├── models.py          # Pydantic models
├── operations/        # CRUD per resource type
├── cli.py             # Typer CLI
├── mcp_server.py      # FastMCP server
└── utils/             # Diff & export helpers
```
