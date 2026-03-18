"""Trigger operations — CRUD."""

from gtm.client import GTMClient
from gtm.models import Trigger


def _workspace_path(client: GTMClient, container_id: str, workspace_id: str = "0") -> str:
    return f"{client.account_path}/containers/{container_id}/workspaces/{workspace_id}"


def list_triggers(client: GTMClient, container_id: str, workspace_id: str = "0") -> list[Trigger]:
    """List all triggers in a workspace."""
    path = _workspace_path(client, container_id, workspace_id)
    result = client.execute_with_retry(
        client.service.accounts().containers().workspaces().triggers().list(parent=path)
    )
    return [
        Trigger(
            trigger_id=t.get("triggerId"),
            name=t["name"],
            type=t["type"],
            filter=t.get("filter"),
            custom_event_filter=t.get("customEventFilter"),
            notes=t.get("notes"),
        )
        for t in result.get("trigger", [])
    ]


def get_trigger(client: GTMClient, container_id: str, trigger_id: str, workspace_id: str = "0") -> Trigger:
    """Get a single trigger by ID."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/triggers/{trigger_id}"
    t = client.execute_with_retry(
        client.service.accounts().containers().workspaces().triggers().get(path=path)
    )
    return Trigger(
        trigger_id=t.get("triggerId"),
        name=t["name"],
        type=t["type"],
        filter=t.get("filter"),
        custom_event_filter=t.get("customEventFilter"),
        notes=t.get("notes"),
    )


def create_trigger(client: GTMClient, container_id: str, trigger: Trigger, workspace_id: str = "0") -> Trigger:
    """Create a new trigger."""
    path = _workspace_path(client, container_id, workspace_id)
    body = trigger.model_dump(exclude_none=True, exclude={"trigger_id"})
    t = client.execute_with_retry(
        client.service.accounts().containers().workspaces().triggers().create(parent=path, body=body)
    )
    return Trigger(
        trigger_id=t.get("triggerId"),
        name=t["name"],
        type=t["type"],
        filter=t.get("filter"),
        custom_event_filter=t.get("customEventFilter"),
        notes=t.get("notes"),
    )


def update_trigger(
    client: GTMClient, container_id: str, trigger_id: str, trigger: Trigger, workspace_id: str = "0"
) -> Trigger:
    """Update an existing trigger."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/triggers/{trigger_id}"
    body = trigger.model_dump(exclude_none=True, exclude={"trigger_id"})
    t = client.execute_with_retry(
        client.service.accounts().containers().workspaces().triggers().update(path=path, body=body)
    )
    return Trigger(
        trigger_id=t.get("triggerId"),
        name=t["name"],
        type=t["type"],
        filter=t.get("filter"),
        custom_event_filter=t.get("customEventFilter"),
        notes=t.get("notes"),
    )


def delete_trigger(client: GTMClient, container_id: str, trigger_id: str, workspace_id: str = "0") -> None:
    """Delete a trigger."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/triggers/{trigger_id}"
    client.execute_with_retry(
        client.service.accounts().containers().workspaces().triggers().delete(path=path)
    )
