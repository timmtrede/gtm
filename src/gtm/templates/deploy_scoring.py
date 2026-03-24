"""
Deploy scoring model GTM resources — DATA-375.

Creates variables and updates tags needed for the scoring pipeline:
- Web container: dlv.value_eur variable + update ga4.purchase tag
- Server container: ed.value_eur variable

The custom sGTM template (scoring.conversion_probability), the
scoring.adjusted_value variable, and the scoring.label variable
must be created manually in the GTM UI since the API does not
support custom template CRUD.

Usage:
    python -m gtm.templates.deploy_scoring [--dry-run]
"""

import argparse

from gtm.client import GTMClient
from gtm.models import Variable
from gtm.operations.tags import get_tag, update_tag
from gtm.operations.variables import create_variable, list_variables
from gtm.operations.workspaces import create_workspace, list_workspaces

WEB_CONTAINER_ID = "32433317"
SERVER_CONTAINER_ID = "171542205"
SERVER_WORKSPACE_ID = "46"  # DATA-375 workspace

GA4_PURCHASE_TAG_ID = "470"


def find_or_create_workspace(client: GTMClient, container_id: str, name: str, dry_run: bool = False) -> str:
    """Find workspace by name or create it. Returns workspace ID."""
    workspaces = list_workspaces(client, container_id)
    for ws in workspaces:
        if ws.name == name:
            print(f"  Found existing workspace: {ws.name} (ID {ws.workspace_id})")
            return ws.workspace_id

    if dry_run:
        print(f"  [DRY RUN] Would create workspace: {name}")
        return "DRY_RUN"

    ws = create_workspace(client, container_id, name, "DATA-375: New scoring logic for Google Ads conversion values")
    print(f"  Created workspace: {ws.name} (ID {ws.workspace_id})")
    return ws.workspace_id


def variable_exists(client: GTMClient, container_id: str, workspace_id: str, var_name: str) -> bool:
    """Check if a variable with the given name already exists."""
    variables = list_variables(client, container_id, workspace_id)
    return any(v.name == var_name for v in variables)


def deploy_web_container(client: GTMClient, workspace_id: str, dry_run: bool = False):
    """Deploy web container changes: dlv.value_eur + update ga4.purchase tag."""
    print("\n=== Web Container (32433317) ===")

    if dry_run:
        print("  [DRY RUN] Would create variable: dlv.value_eur")
        print(f"  [DRY RUN] Would add value_eur event param to ga4.purchase tag (ID {GA4_PURCHASE_TAG_ID})")
        return

    # 1. Create dlv.value_eur
    var_name = "dlv.value_eur"
    if variable_exists(client, WEB_CONTAINER_ID, workspace_id, var_name):
        print(f"  Variable '{var_name}' already exists, skipping.")
    else:
        var = Variable(
            name=var_name,
            type="v",  # Data Layer Variable
            parameter=[
                {"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
                {"type": "BOOLEAN", "key": "setDefaultValue", "value": "false"},
                {"type": "TEMPLATE", "key": "name", "value": "value_eur"},
            ],
            notes="DATA-375: EUR value for scoring model net_revenue_first_transport",
        )
        result = create_variable(client, WEB_CONTAINER_ID, var, workspace_id)
        print(f"  Created variable: {var_name} (ID {result.variable_id})")

    # 2. Update ga4.purchase tag to add value_eur event parameter
    print(f"\n  Updating ga4.purchase tag (ID {GA4_PURCHASE_TAG_ID})...")
    tag = get_tag(client, WEB_CONTAINER_ID, GA4_PURCHASE_TAG_ID, workspace_id)
    print(f"  Current tag: {tag.name} (type: {tag.type})")

    # Find the eventSettingsTable parameter and add value_eur
    params = tag.parameter or []
    event_settings_param = None
    for p in params:
        if p.get("key") == "eventSettingsTable":
            event_settings_param = p
            break

    if event_settings_param is None:
        print("  ERROR: Could not find eventSettingsTable parameter on ga4.purchase tag")
        return

    # Check if value_eur is already in the event settings
    rows = event_settings_param.get("list", [])
    has_value_eur = False
    for row in rows:
        row_map = row.get("map", [])
        for entry in row_map:
            if entry.get("key") == "parameter" and entry.get("value") == "value_eur":
                has_value_eur = True
                break

    if has_value_eur:
        print("  value_eur already in eventSettingsTable, skipping.")
    else:
        new_row = {
            "type": "MAP",
            "map": [
                {"type": "TEMPLATE", "key": "parameter", "value": "value_eur"},
                {"type": "TEMPLATE", "key": "parameterValue", "value": "{{dlv.value_eur}}"},
            ],
        }
        rows.append(new_row)
        event_settings_param["list"] = rows
        updated_tag = update_tag(client, WEB_CONTAINER_ID, GA4_PURCHASE_TAG_ID, tag, workspace_id)
        print(f"  Updated tag: {updated_tag.name} — added value_eur event parameter")


def deploy_server_container(client: GTMClient, dry_run: bool = False):
    """Deploy server container changes: ed.value_eur."""
    print(f"\n=== Server Container (171542205) — Workspace {SERVER_WORKSPACE_ID} ===")

    # 1. Create ed.value_eur
    var_name = "ed.value_eur"
    if dry_run:
        print(f"  [DRY RUN] Would create variable: {var_name}")
        return

    if variable_exists(client, SERVER_CONTAINER_ID, SERVER_WORKSPACE_ID, var_name):
        print(f"  Variable '{var_name}' already exists, skipping.")
    else:
        var = Variable(
            name=var_name,
            type="ed",  # Event Data variable (server-side)
            parameter=[
                {"type": "boolean", "key": "setDefaultValue", "value": "false"},
                {"type": "template", "key": "keyPath", "value": "value_eur"},
            ],
            notes="DATA-375: EUR value from purchase event for scoring model",
        )
        result = create_variable(client, SERVER_CONTAINER_ID, var, SERVER_WORKSPACE_ID)
        print(f"  Created variable: {var_name} (ID {result.variable_id})")


def main():
    parser = argparse.ArgumentParser(description="Deploy DATA-375 scoring GTM resources")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()

    client = GTMClient()
    print("DATA-375: Deploying scoring model GTM resources")
    if args.dry_run:
        print("[DRY RUN MODE — no changes will be made]")

    # Web container: find or create workspace
    print("\nFinding/creating web container workspace...")
    web_workspace_id = find_or_create_workspace(
        client, WEB_CONTAINER_ID, "DATA-375 New scoring logic for Gads Transaction Values",
        dry_run=args.dry_run,
    )

    # Deploy
    deploy_web_container(client, web_workspace_id, args.dry_run)
    deploy_server_container(client, args.dry_run)

    print("\n=== Summary ===")
    print("Web container:")
    print("  - dlv.value_eur variable")
    print("  - ga4.purchase tag updated with value_eur event param")
    print("Server container:")
    print("  - ed.value_eur variable")
    print("\nManual steps remaining:")
    print("  1. Create scoring.conversion_probability custom variable template in GTM UI")
    print("     (code in: src/gtm/templates/sgtm_scoring_conversion_probability.tpl)")
    print("  2. Create scoring.adjusted_value variable in GTM UI")
    print("     (formula: clamp(prob * 3, 0.6, 2.4) * ed.value)")
    print("  3. Create scoring.label variable in GTM UI")
    print("     (buckets: <0.8 -> b_kunden, [0.8,1.2] -> a_kunden, >1.2 -> a_plus_kunden)")
    print("  4. Update alookup.gads_variable_value (variable 177)")
    print("  5. Update alookup.gads_variable_label (variable 258)")
    print("  6. Delete tr.value.70% (ID 270) and firestore.scores.purchase (ID 250)")


if __name__ == "__main__":
    main()
