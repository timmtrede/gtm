"""Version operations — create, publish, diff, rollback."""

from gtm.client import GTMClient
from gtm.models import VersionDiff


def _container_path(client: GTMClient, container_id: str) -> str:
    return f"{client.account_path}/containers/{container_id}"


def list_versions(client: GTMClient, container_id: str) -> list[dict]:
    """List all versions (headers only) for a container."""
    path = _container_path(client, container_id)
    result = client.execute_with_retry(
        client.service.accounts().containers().version_headers().list(parent=path)
    )
    return result.get("containerVersionHeader", [])


def get_version(client: GTMClient, container_id: str, version_id: str) -> dict:
    """Get a full version by ID."""
    path = f"{_container_path(client, container_id)}/versions/{version_id}"
    return client.execute_with_retry(
        client.service.accounts().containers().versions().get(path=path)
    )


def get_live_version(client: GTMClient, container_id: str) -> dict:
    """Get the currently published (live) version."""
    return client.execute_with_retry(
        client.service.accounts().containers().versions().live(parent=_container_path(client, container_id))
    )


def create_version(client: GTMClient, container_id: str, workspace_id: str, name: str, notes: str = "") -> dict:
    """Create a new version from a workspace."""
    path = f"{_container_path(client, container_id)}/workspaces/{workspace_id}"
    body = {"name": name, "notes": notes}
    result = client.execute_with_retry(
        client.service.accounts()
        .containers()
        .workspaces()
        .create_version(path=path, body=body)
    )
    return result.get("containerVersion", {})


def publish_version(client: GTMClient, container_id: str, version_id: str) -> dict:
    """Publish a version (make it live)."""
    path = f"{_container_path(client, container_id)}/versions/{version_id}"
    return client.execute_with_retry(
        client.service.accounts().containers().versions().publish(path=path)
    )


def diff_versions(client: GTMClient, container_id: str, version_a_id: str, version_b_id: str) -> VersionDiff:
    """Diff two versions and return structured changes."""
    from deepdiff import DeepDiff

    va = get_version(client, container_id, version_a_id)
    vb = get_version(client, container_id, version_b_id)

    def _names(version_data: dict, key: str) -> dict[str, dict]:
        return {item["name"]: item for item in version_data.get(key, [])}

    diff = VersionDiff(version_a=version_a_id, version_b=version_b_id)

    for resource_key, added_attr, removed_attr, modified_attr in [
        ("tag", "added_tags", "removed_tags", "modified_tags"),
        ("trigger", "added_triggers", "removed_triggers", "modified_triggers"),
        ("variable", "added_variables", "removed_variables", "modified_variables"),
    ]:
        names_a = _names(va, resource_key)
        names_b = _names(vb, resource_key)

        setattr(diff, added_attr, sorted(set(names_b) - set(names_a)))
        setattr(diff, removed_attr, sorted(set(names_a) - set(names_b)))

        common = set(names_a) & set(names_b)
        modified = []
        for name in sorted(common):
            if DeepDiff(names_a[name], names_b[name], ignore_order=True):
                modified.append(name)
        setattr(diff, modified_attr, modified)

    return diff
