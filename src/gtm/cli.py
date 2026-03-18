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


if __name__ == "__main__":
    app()
