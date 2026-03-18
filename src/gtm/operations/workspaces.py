"""Workspace operations."""

from gtm.client import GTMClient
from gtm.models import Workspace


def _container_path(client: GTMClient, container_id: str) -> str:
    return f"{client.account_path}/containers/{container_id}"


def list_workspaces(client: GTMClient, container_id: str) -> list[Workspace]:
    """List all workspaces in a container."""
    path = _container_path(client, container_id)
    result = client.execute_with_retry(
        client.service.accounts().containers().workspaces().list(parent=path)
    )
    return [
        Workspace(
            workspace_id=w.get("workspaceId"),
            name=w["name"],
            description=w.get("description"),
        )
        for w in result.get("workspace", [])
    ]


def create_workspace(client: GTMClient, container_id: str, name: str, description: str = "") -> Workspace:
    """Create a new workspace."""
    path = _container_path(client, container_id)
    body = {"name": name, "description": description}
    w = client.execute_with_retry(
        client.service.accounts().containers().workspaces().create(parent=path, body=body)
    )
    return Workspace(
        workspace_id=w.get("workspaceId"),
        name=w["name"],
        description=w.get("description"),
    )


def delete_workspace(client: GTMClient, container_id: str, workspace_id: str) -> None:
    """Delete a workspace."""
    path = f"{_container_path(client, container_id)}/workspaces/{workspace_id}"
    client.execute_with_retry(
        client.service.accounts().containers().workspaces().delete(path=path)
    )
