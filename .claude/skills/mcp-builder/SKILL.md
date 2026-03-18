# MCP Server Builder

Guide for building FastMCP servers that expose tools for Claude Code.

## Pattern
```python
from fastmcp import FastMCP

mcp = FastMCP("server-name", instructions="What this server does")

@mcp.tool(description="...", annotations={"readOnlyHint": True})
def my_read_tool(param: str) -> dict:
    ...

@mcp.tool(description="... — DESTRUCTIVE", annotations={"destructiveHint": True})
def my_write_tool(param: str) -> str:
    ...
```

## Annotations
- `readOnlyHint: True` — tool only reads data, safe to auto-approve
- `destructiveHint: True` — tool modifies/deletes data, should require confirmation

## Registration
Add to `.mcp.json` at project root:
```json
{
  "mcpServers": {
    "name": {
      "command": "python",
      "args": ["-m", "module.mcp_server"],
      "cwd": "/path/to/project"
    }
  }
}
```
