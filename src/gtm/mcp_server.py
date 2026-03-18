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


# --- Firestore ---


def _fs_client():
    from gtm.firestore_client import FirestoreClient

    return FirestoreClient()


@mcp.tool(
    description="List all Firestore collections with document counts",
    annotations={"readOnlyHint": True},
)
def firestore_list_collections() -> list[dict]:
    from gtm.operations.firestore_ops import list_collections

    return list_collections(_fs_client())


@mcp.tool(
    description="Query GTM server container events. Filter by event_name, user_id, or transaction_id.",
    annotations={"readOnlyHint": True},
)
def firestore_query_events(
    event_name: str = "",
    user_id: str = "",
    transaction_id: str = "",
    limit: int = 20,
) -> list[dict]:
    from gtm.operations.firestore_ops import query_events

    return query_events(
        _fs_client(),
        event_name=event_name or None,
        user_id=user_id or None,
        transaction_id=transaction_id or None,
        limit=limit,
    )


@mcp.tool(
    description="Get a single event document by Firestore document ID",
    annotations={"readOnlyHint": True},
)
def firestore_get_event(doc_id: str) -> dict | None:
    from gtm.operations.firestore_ops import get_event

    return get_event(_fs_client(), doc_id)


@mcp.tool(
    description="List or lookup existing customers. Provide user_id to filter.",
    annotations={"readOnlyHint": True},
)
def firestore_customers(user_id: str = "", limit: int = 50) -> list[dict]:
    from gtm.operations.firestore_ops import list_customers, lookup_customer

    if user_id:
        return lookup_customer(_fs_client(), user_id)
    return list_customers(_fs_client(), limit=limit)


@mcp.tool(
    description="Get the lead score for a company domain",
    annotations={"readOnlyHint": True},
)
def firestore_get_score(domain: str) -> dict | None:
    from gtm.operations.firestore_ops import get_score

    return get_score(_fs_client(), domain)


@mcp.tool(
    description="List lead score documents",
    annotations={"readOnlyHint": True},
)
def firestore_list_scores(limit: int = 20) -> list[dict]:
    from gtm.operations.firestore_ops import query_scores

    return query_scores(_fs_client(), limit=limit)


@mcp.tool(
    description="Check if a domain is in the generic email domains list (e.g. gmail.com)",
    annotations={"readOnlyHint": True},
)
def firestore_is_generic_domain(domain: str) -> dict:
    from gtm.operations.firestore_ops import is_generic_domain

    return {"domain": domain, "is_generic": is_generic_domain(_fs_client(), domain)}


@mcp.tool(
    description="Run a generic query on any Firestore collection with optional field filter",
    annotations={"readOnlyHint": True},
)
def firestore_query(
    collection: str,
    field: str = "",
    op: str = "==",
    value: str = "",
    limit: int = 20,
) -> list[dict]:
    from gtm.operations.firestore_ops import query_collection

    return query_collection(
        _fs_client(),
        collection,
        field=field or None,
        op=op,
        value=value or None,
        limit=limit,
    )


# --- BigQuery ---


def _bq_client():
    from gtm.bigquery_client import BigQueryClient

    return BigQueryClient()


@mcp.tool(
    description="List all BigQuery datasets in the project",
    annotations={"readOnlyHint": True},
)
def bigquery_list_datasets() -> list[dict]:
    from gtm.operations.bigquery_ops import list_datasets

    return list_datasets(_bq_client())


@mcp.tool(
    description="List all tables in a BigQuery dataset",
    annotations={"readOnlyHint": True},
)
def bigquery_list_tables(dataset_id: str) -> list[dict]:
    from gtm.operations.bigquery_ops import list_tables

    return list_tables(_bq_client(), dataset_id)


@mcp.tool(
    description="Get schema and metadata for a BigQuery table (columns, types, row count, size)",
    annotations={"readOnlyHint": True},
)
def bigquery_get_table_schema(dataset_id: str, table_id: str) -> dict:
    from gtm.operations.bigquery_ops import get_table_schema

    return get_table_schema(_bq_client(), dataset_id, table_id)


@mcp.tool(
    description="Preview rows from a BigQuery table without running a query",
    annotations={"readOnlyHint": True},
)
def bigquery_preview_table(dataset_id: str, table_id: str, limit: int = 10) -> list[dict]:
    from gtm.operations.bigquery_ops import preview_table

    return preview_table(_bq_client(), dataset_id, table_id, limit=limit)


@mcp.tool(
    description="Run a read-only SQL query on BigQuery. Has a 10 GB safety limit.",
    annotations={"readOnlyHint": True},
)
def bigquery_query(sql: str, limit: int = 100) -> dict:
    from gtm.operations.bigquery_ops import run_query

    return run_query(_bq_client(), sql, limit=limit)


@mcp.tool(
    description="Dry-run a BigQuery SQL query to estimate bytes processed without executing",
    annotations={"readOnlyHint": True},
)
def bigquery_dry_run(sql: str) -> dict:
    from gtm.operations.bigquery_ops import dry_run_query

    return dry_run_query(_bq_client(), sql)


if __name__ == "__main__":
    mcp.run()
