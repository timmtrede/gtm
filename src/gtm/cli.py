"""GTM CLI — Typer-based command-line interface."""

from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

app = typer.Typer(name="gtm", help="GTM-as-Code CLI for Google Tag Manager management")
console = Console()


def _client():
    from gtm.client import GTMClient

    return GTMClient()


# --- Containers ---

containers_app = typer.Typer(help="Container operations")
app.add_typer(containers_app, name="containers")


@containers_app.command("list")
def containers_list():
    """List all containers in the account."""
    from gtm.operations.containers import list_containers

    containers = list_containers(_client())
    table = Table(title="GTM Containers")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Public ID")
    table.add_column("Domains")
    for c in containers:
        table.add_row(c.container_id, c.name, c.public_id or "", ", ".join(c.domain_name))
    console.print(table)


@containers_app.command("export")
def containers_export(
    container_id: str = typer.Argument(help="Container ID to export"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory"),
):
    """Export the live container version as JSON."""
    from gtm.operations.containers import export_container

    out = Path(output_dir) if output_dir else None
    path = export_container(_client(), container_id, out)
    console.print(f"Exported to [green]{path}[/green]")


# --- Tags ---

tags_app = typer.Typer(help="Tag operations")
app.add_typer(tags_app, name="tags")


@tags_app.command("list")
def tags_list(
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
    workspace_id: str = typer.Option("0", "--workspace", "-w", help="Workspace ID"),
):
    """List all tags in a container workspace."""
    from gtm.operations.tags import list_tags

    tags = list_tags(_client(), container_id, workspace_id)
    table = Table(title=f"Tags in container {container_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    table.add_column("Paused")
    for t in tags:
        table.add_row(t.tag_id or "", t.name, t.type, "Yes" if t.paused else "")
    console.print(table)


@tags_app.command("search")
def tags_search(
    query: str = typer.Argument(help="Search query"),
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
    workspace_id: str = typer.Option("0", "--workspace", "-w", help="Workspace ID"),
):
    """Search tags by name."""
    from gtm.operations.tags import search_tags

    tags = search_tags(_client(), container_id, query, workspace_id)
    for t in tags:
        console.print(f"  [{t.tag_id}] {t.name} ({t.type})")


# --- Triggers ---

triggers_app = typer.Typer(help="Trigger operations")
app.add_typer(triggers_app, name="triggers")


@triggers_app.command("list")
def triggers_list(
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
    workspace_id: str = typer.Option("0", "--workspace", "-w", help="Workspace ID"),
):
    """List all triggers in a container workspace."""
    from gtm.operations.triggers import list_triggers

    triggers = list_triggers(_client(), container_id, workspace_id)
    table = Table(title=f"Triggers in container {container_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    for t in triggers:
        table.add_row(t.trigger_id or "", t.name, t.type)
    console.print(table)


# --- Variables ---

variables_app = typer.Typer(help="Variable operations")
app.add_typer(variables_app, name="variables")


@variables_app.command("list")
def variables_list(
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
    workspace_id: str = typer.Option("0", "--workspace", "-w", help="Workspace ID"),
):
    """List all variables in a container workspace."""
    from gtm.operations.variables import list_variables

    variables = list_variables(_client(), container_id, workspace_id)
    table = Table(title=f"Variables in container {container_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Type")
    for v in variables:
        table.add_row(v.variable_id or "", v.name, v.type)
    console.print(table)


# --- Versions ---

versions_app = typer.Typer(help="Version operations")
app.add_typer(versions_app, name="versions")


@versions_app.command("list")
def versions_list(
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
):
    """List all versions of a container."""
    from gtm.operations.versions import list_versions

    versions = list_versions(_client(), container_id)
    table = Table(title=f"Versions for container {container_id}")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Deleted")
    for v in versions:
        table.add_row(
            v.get("containerVersionId", ""),
            v.get("name", ""),
            "Yes" if v.get("deleted") else "",
        )
    console.print(table)


@versions_app.command("diff")
def versions_diff(
    version_a: str = typer.Argument(help="First version ID"),
    version_b: str = typer.Argument(help="Second version ID"),
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
):
    """Diff two container versions."""
    from gtm.operations.versions import diff_versions

    diff = diff_versions(_client(), container_id, version_a, version_b)
    console.print(f"\n[bold]Version {diff.version_a} → {diff.version_b}[/bold]\n")
    for label, items in [
        ("Added tags", diff.added_tags),
        ("Removed tags", diff.removed_tags),
        ("Modified tags", diff.modified_tags),
        ("Added triggers", diff.added_triggers),
        ("Removed triggers", diff.removed_triggers),
        ("Modified triggers", diff.modified_triggers),
        ("Added variables", diff.added_variables),
        ("Removed variables", diff.removed_variables),
        ("Modified variables", diff.modified_variables),
    ]:
        if items:
            console.print(f"  [bold]{label}:[/bold]")
            for item in items:
                console.print(f"    - {item}")


# --- Audit ---

@app.command("audit")
def audit(
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
    workspace_id: str = typer.Option("0", "--workspace", "-w", help="Workspace ID"),
):
    """Run an audit on a container."""
    from gtm.operations.audit import audit_container

    result = audit_container(_client(), container_id, workspace_id)
    console.print(f"\n[bold]Audit: {result.container_name}[/bold]")
    console.print(
        f"  Tags: {result.tags_count} | Triggers: {result.triggers_count} | Variables: {result.variables_count}"
    )
    console.print(f"  Errors: {result.error_count} | Warnings: {result.warning_count}\n")

    for f in result.findings:
        color = {"error": "red", "warning": "yellow", "info": "blue"}[f.severity]
        console.print(f"  [{color}][{f.severity.upper()}][/{color}] {f.resource_type}/{f.resource_name}: {f.message}")


# --- Backup ---

@app.command("backup")
def backup(
    container_id: str = typer.Option(..., "--container", "-c", help="Container ID"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory"),
):
    """Backup the live container version to a JSON file."""
    from gtm.operations.containers import export_container

    out = Path(output_dir) if output_dir else None
    path = export_container(_client(), container_id, out)
    console.print(f"Backed up to [green]{path}[/green]")


# --- Firestore ---

firestore_app = typer.Typer(help="Firestore operations (GTM server container data)")
app.add_typer(firestore_app, name="firestore")


def _fs_client():
    from gtm.firestore_client import FirestoreClient

    return FirestoreClient()


@firestore_app.command("collections")
def firestore_collections():
    """List all Firestore collections with document counts."""
    from gtm.operations.firestore_ops import list_collections

    collections = list_collections(_fs_client())
    table = Table(title="Firestore Collections")
    table.add_column("Collection", style="bold")
    table.add_column("Documents", style="cyan", justify="right")
    for c in collections:
        table.add_row(c["name"], f"{c['document_count']:,}")
    console.print(table)


@firestore_app.command("events")
def firestore_events(
    event_name: str = typer.Option(None, "--event", "-e", help="Filter by event_name"),
    user_id: str = typer.Option(None, "--user", "-u", help="Filter by user_id"),
    transaction_id: str = typer.Option(None, "--txn", "-t", help="Filter by transaction_id"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max results"),
):
    """Query GTM server container events."""
    from gtm.operations.firestore_ops import query_events

    events = query_events(
        _fs_client(), event_name=event_name, user_id=user_id, transaction_id=transaction_id, limit=limit
    )
    table = Table(title=f"Events ({len(events)} results)")
    table.add_column("Doc ID", style="cyan")
    table.add_column("Event", style="bold")
    table.add_column("User ID")
    table.add_column("Transaction")
    table.add_column("Value")
    table.add_column("Currency")
    for e in events:
        table.add_row(
            e.get("_id", ""),
            e.get("event_name", ""),
            e.get("user_id", ""),
            e.get("transaction_id", ""),
            str(e.get("value", "")) if e.get("value") else "",
            e.get("currency", ""),
        )
    console.print(table)


@firestore_app.command("event")
def firestore_event(doc_id: str = typer.Argument(help="Document ID")):
    """Get a single event document by ID."""
    import json

    from gtm.operations.firestore_ops import get_event

    event = get_event(_fs_client(), doc_id)
    if event:
        console.print_json(json.dumps(event, default=str))
    else:
        console.print(f"[red]Document {doc_id} not found[/red]")


@firestore_app.command("customers")
def firestore_customers(
    user_id: str = typer.Option(None, "--user", "-u", help="Lookup by user_id"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max results"),
):
    """List or lookup existing customers."""
    from gtm.operations.firestore_ops import list_customers, lookup_customer

    if user_id:
        customers = lookup_customer(_fs_client(), user_id)
    else:
        customers = list_customers(_fs_client(), limit=limit)

    table = Table(title=f"Existing Customers ({len(customers)} results)")
    table.add_column("Doc ID", style="cyan")
    table.add_column("User ID", style="bold")
    table.add_column("Timestamp")
    for c in customers:
        table.add_row(c.get("_id", ""), c.get("user_id", ""), str(c.get("timestamp", "")))
    console.print(table)


@firestore_app.command("score")
def firestore_score(domain: str = typer.Argument(help="Domain to look up")):
    """Get the lead score for a domain."""
    import json

    from gtm.operations.firestore_ops import get_score

    score = get_score(_fs_client(), domain)
    if score:
        console.print_json(json.dumps(score, default=str))
    else:
        console.print(f"[red]No score found for {domain}[/red]")


@firestore_app.command("scores")
def firestore_scores(limit: int = typer.Option(20, "--limit", "-n", help="Max results")):
    """List lead score documents."""
    from gtm.operations.firestore_ops import query_scores

    scores = query_scores(_fs_client(), limit=limit)
    table = Table(title=f"Scores ({len(scores)} results)")
    table.add_column("Domain", style="cyan")
    table.add_column("Score", style="bold")
    table.add_column("Industry")
    table.add_column("B2C")
    for s in scores:
        table.add_row(
            s.get("_id", ""),
            str(s.get("score", s.get("new_scoring", ""))),
            s.get("company_industry", ""),
            str(s.get("mainly_b2c", "")),
        )
    console.print(table)


@firestore_app.command("domains")
def firestore_domains(
    check: str = typer.Option(None, "--check", help="Check if a domain is generic"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max results"),
):
    """List generic email domains or check a specific one."""
    from gtm.operations.firestore_ops import is_generic_domain, list_generic_domains

    if check:
        is_generic = is_generic_domain(_fs_client(), check)
        if is_generic:
            console.print(f"[yellow]{check}[/yellow] is a generic domain")
        else:
            console.print(f"[green]{check}[/green] is NOT a generic domain")
    else:
        domains = list_generic_domains(_fs_client(), limit=limit)
        for d in domains:
            console.print(f"  {d}")
        console.print(f"\n[dim]Showing {len(domains)} of total[/dim]")


@firestore_app.command("query")
def firestore_query(
    collection: str = typer.Argument(help="Collection name"),
    field: str = typer.Option(None, "--field", "-f", help="Field to filter on"),
    op: str = typer.Option("==", "--op", help="Comparison operator (==, !=, <, >, <=, >=)"),
    value: str = typer.Option(None, "--value", "-v", help="Value to compare"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max results"),
):
    """Run a generic query on any Firestore collection."""
    import json

    from gtm.operations.firestore_ops import query_collection

    results = query_collection(_fs_client(), collection, field=field, op=op, value=value, limit=limit)
    console.print(f"\n[bold]{len(results)} results from {collection}[/bold]\n")
    for doc in results:
        console.print_json(json.dumps(doc, default=str))
        console.print()


# --- BigQuery ---

bq_app = typer.Typer(help="BigQuery operations (read-only)")
app.add_typer(bq_app, name="bq")


def _bq_client():
    from gtm.bigquery_client import BigQueryClient

    return BigQueryClient()


@bq_app.command("datasets")
def bq_datasets():
    """List all BigQuery datasets."""
    from gtm.operations.bigquery_ops import list_datasets

    datasets = list_datasets(_bq_client())
    table = Table(title="BigQuery Datasets")
    table.add_column("Dataset", style="bold")
    for ds in datasets:
        table.add_row(ds["dataset_id"])
    console.print(table)


@bq_app.command("tables")
def bq_tables(dataset: str = typer.Argument(help="Dataset ID")):
    """List all tables in a dataset."""
    from gtm.operations.bigquery_ops import list_tables

    tables = list_tables(_bq_client(), dataset)
    table = Table(title=f"Tables in {dataset}")
    table.add_column("Table", style="bold")
    table.add_column("Type", style="cyan")
    for t in tables:
        table.add_row(t["table_id"], t["table_type"])
    console.print(table)


@bq_app.command("schema")
def bq_schema(
    dataset: str = typer.Argument(help="Dataset ID"),
    table_name: str = typer.Argument(help="Table ID"),
):
    """Show schema and metadata for a table."""
    from gtm.operations.bigquery_ops import get_table_schema

    info = get_table_schema(_bq_client(), dataset, table_name)
    console.print(f"\n[bold]{dataset}.{table_name}[/bold]")
    console.print(f"  Type: {info['table_type']} | Rows: {info['num_rows']:,} | Size: {info['num_bytes']:,} bytes")
    if info["description"]:
        console.print(f"  Description: {info['description']}")
    console.print()

    table = Table(title="Schema")
    table.add_column("Field", style="bold")
    table.add_column("Type", style="cyan")
    table.add_column("Mode")
    table.add_column("Description")
    for f in info["schema"]:
        table.add_row(f["name"], f["type"], f["mode"], f["description"] or "")
    console.print(table)


@bq_app.command("preview")
def bq_preview(
    dataset: str = typer.Argument(help="Dataset ID"),
    table_name: str = typer.Argument(help="Table ID"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max rows"),
):
    """Preview rows from a table."""
    import json

    from gtm.operations.bigquery_ops import preview_table

    rows = preview_table(_bq_client(), dataset, table_name, limit=limit)
    console.print(f"\n[bold]{dataset}.{table_name}[/bold] — {len(rows)} rows\n")
    for row in rows:
        console.print_json(json.dumps(row, default=str))
        console.print()


@bq_app.command("query")
def bq_query(
    sql: str = typer.Argument(help="SQL query to run"),
    limit: int = typer.Option(100, "--limit", "-n", help="Max rows"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Estimate bytes without executing"),
):
    """Run a read-only SQL query."""
    import json

    from gtm.operations.bigquery_ops import dry_run_query, run_query

    if dry_run:
        info = dry_run_query(_bq_client(), sql)
        console.print(f"Estimated bytes: [bold]{info['total_bytes_processed_human']}[/bold]")
        return

    result = run_query(_bq_client(), sql, limit=limit)
    console.print(
        f"\n[dim]{result['total_rows']} total rows | "
        f"{result['bytes_processed']:,} bytes processed | "
        f"cache: {result['cache_hit']}[/dim]\n"
    )
    for row in result["rows"]:
        console.print_json(json.dumps(row, default=str))
        console.print()


if __name__ == "__main__":
    app()
