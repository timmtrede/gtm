"""FastMCP server exposing GTM operations as tools."""

from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("gtm", instructions="Google Tag Manager management tools for the Zipmend GTM account.")


def _client():
    from gtm.client import GTMClient

    return GTMClient()


# --- Containers (read-only) ---


@mcp.tool(
    description="List all GTM containers in the account",
    annotations={"readOnlyHint": True},
)
def list_containers() -> list[dict]:
    from gtm.operations.containers import list_containers as _list

    return [c.model_dump() for c in _list(_client())]


@mcp.tool(
    description="Get details for a specific container",
    annotations={"readOnlyHint": True},
)
def get_container(container_id: str) -> dict:
    from gtm.operations.containers import get_container as _get

    return _get(_client(), container_id).model_dump()


@mcp.tool(
    description="Export the live container version as JSON backup",
)
def export_container(container_id: str) -> str:
    from gtm.operations.containers import export_container as _export

    path = _export(_client(), container_id)
    return f"Exported to {path}"


# --- Tags ---


@mcp.tool(
    description="List all tags in a container workspace",
    annotations={"readOnlyHint": True},
)
def list_tags(container_id: str, workspace_id: str = "0") -> list[dict]:
    from gtm.operations.tags import list_tags as _list

    return [t.model_dump() for t in _list(_client(), container_id, workspace_id)]


@mcp.tool(
    description="Get a specific tag by ID",
    annotations={"readOnlyHint": True},
)
def get_tag(container_id: str, tag_id: str, workspace_id: str = "0") -> dict:
    from gtm.operations.tags import get_tag as _get

    return _get(_client(), container_id, tag_id, workspace_id).model_dump()


@mcp.tool(
    description="Search tags by name (case-insensitive)",
    annotations={"readOnlyHint": True},
)
def search_tags(container_id: str, query: str, workspace_id: str = "0") -> list[dict]:
    from gtm.operations.tags import search_tags as _search

    return [t.model_dump() for t in _search(_client(), container_id, query, workspace_id)]


@mcp.tool(
    description="Create a new tag in a container workspace",
)
def create_tag(container_id: str, name: str, tag_type: str, workspace_id: str = "0") -> dict:
    from gtm.models import Tag
    from gtm.operations.tags import create_tag as _create

    tag = Tag(name=name, type=tag_type)
    return _create(_client(), container_id, tag, workspace_id).model_dump()


@mcp.tool(
    description="Delete a tag — DESTRUCTIVE operation",
    annotations={"destructiveHint": True},
)
def delete_tag(container_id: str, tag_id: str, workspace_id: str = "0") -> str:
    from gtm.operations.tags import delete_tag as _delete

    _delete(_client(), container_id, tag_id, workspace_id)
    return f"Tag {tag_id} deleted"


# --- Triggers ---


@mcp.tool(
    description="List all triggers in a container workspace",
    annotations={"readOnlyHint": True},
)
def list_triggers(container_id: str, workspace_id: str = "0") -> list[dict]:
    from gtm.operations.triggers import list_triggers as _list

    return [t.model_dump() for t in _list(_client(), container_id, workspace_id)]


@mcp.tool(
    description="Create a new trigger",
)
def create_trigger(container_id: str, name: str, trigger_type: str, workspace_id: str = "0") -> dict:
    from gtm.models import Trigger
    from gtm.operations.triggers import create_trigger as _create

    trigger = Trigger(name=name, type=trigger_type)
    return _create(_client(), container_id, trigger, workspace_id).model_dump()


@mcp.tool(
    description="Delete a trigger — DESTRUCTIVE operation",
    annotations={"destructiveHint": True},
)
def delete_trigger(container_id: str, trigger_id: str, workspace_id: str = "0") -> str:
    from gtm.operations.triggers import delete_trigger as _delete

    _delete(_client(), container_id, trigger_id, workspace_id)
    return f"Trigger {trigger_id} deleted"


# --- Variables ---


@mcp.tool(
    description="List all variables in a container workspace",
    annotations={"readOnlyHint": True},
)
def list_variables(container_id: str, workspace_id: str = "0") -> list[dict]:
    from gtm.operations.variables import list_variables as _list

    return [t.model_dump() for t in _list(_client(), container_id, workspace_id)]


@mcp.tool(
    description="Create a new variable",
)
def create_variable(container_id: str, name: str, variable_type: str, workspace_id: str = "0") -> dict:
    from gtm.models import Variable
    from gtm.operations.variables import create_variable as _create

    variable = Variable(name=name, type=variable_type)
    return _create(_client(), container_id, variable, workspace_id).model_dump()


@mcp.tool(
    description="Delete a variable — DESTRUCTIVE operation",
    annotations={"destructiveHint": True},
)
def delete_variable(container_id: str, variable_id: str, workspace_id: str = "0") -> str:
    from gtm.operations.variables import delete_variable as _delete

    _delete(_client(), container_id, variable_id, workspace_id)
    return f"Variable {variable_id} deleted"


# --- Versions ---


@mcp.tool(
    description="List all versions of a container",
    annotations={"readOnlyHint": True},
)
def list_versions(container_id: str) -> list[dict]:
    from gtm.operations.versions import list_versions as _list

    return _list(_client(), container_id)


@mcp.tool(
    description="Get the live (published) version of a container",
    annotations={"readOnlyHint": True},
)
def get_live_version(container_id: str) -> dict:
    from gtm.operations.versions import get_live_version as _get

    return _get(_client(), container_id)


@mcp.tool(
    description="Diff two container versions",
    annotations={"readOnlyHint": True},
)
def diff_versions(container_id: str, version_a: str, version_b: str) -> dict:
    from gtm.operations.versions import diff_versions as _diff

    return _diff(_client(), container_id, version_a, version_b).model_dump()


@mcp.tool(
    description="Create a new version from a workspace",
)
def create_version(container_id: str, workspace_id: str, name: str, notes: str = "") -> dict:
    from gtm.operations.versions import create_version as _create

    return _create(_client(), container_id, workspace_id, name, notes)


@mcp.tool(
    description="Publish a version (make it live) — DESTRUCTIVE operation",
    annotations={"destructiveHint": True},
)
def publish_version(container_id: str, version_id: str) -> dict:
    from gtm.operations.versions import publish_version as _publish

    return _publish(_client(), container_id, version_id)


# --- Workspaces ---


@mcp.tool(
    description="List all workspaces in a container",
    annotations={"readOnlyHint": True},
)
def list_workspaces(container_id: str) -> list[dict]:
    from gtm.operations.workspaces import list_workspaces as _list

    return [w.model_dump() for w in _list(_client(), container_id)]


@mcp.tool(
    description="Create a new workspace",
)
def create_workspace(container_id: str, name: str, description: str = "") -> dict:
    from gtm.operations.workspaces import create_workspace as _create

    return _create(_client(), container_id, name, description).model_dump()


# --- Audit ---


@mcp.tool(
    description="Run a full audit on a container — checks naming, unused items, duplicates",
    annotations={"readOnlyHint": True},
)
def audit_container(container_id: str, workspace_id: str = "0") -> dict:
    from gtm.operations.audit import audit_container as _audit

    return _audit(_client(), container_id, workspace_id).model_dump()


if __name__ == "__main__":
    mcp.run()
