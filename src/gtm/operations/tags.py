"""Tag operations — CRUD and search."""

from gtm.client import GTMClient
from gtm.models import Tag


def _workspace_path(client: GTMClient, container_id: str, workspace_id: str = "0") -> str:
    return f"{client.account_path}/containers/{container_id}/workspaces/{workspace_id}"


def list_tags(client: GTMClient, container_id: str, workspace_id: str = "0") -> list[Tag]:
    """List all tags in a workspace (default: default workspace)."""
    path = _workspace_path(client, container_id, workspace_id)
    result = client.execute_with_retry(
        client.service.accounts().containers().workspaces().tags().list(parent=path)
    )
    return [
        Tag(
            tag_id=t.get("tagId"),
            name=t["name"],
            type=t["type"],
            parameter=t.get("parameter"),
            firing_trigger_id=t.get("firingTriggerId", []),
            blocking_trigger_id=t.get("blockingTriggerId", []),
            paused=t.get("paused", False),
            notes=t.get("notes"),
        )
        for t in result.get("tag", [])
    ]


def get_tag(client: GTMClient, container_id: str, tag_id: str, workspace_id: str = "0") -> Tag:
    """Get a single tag by ID."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/tags/{tag_id}"
    t = client.execute_with_retry(
        client.service.accounts().containers().workspaces().tags().get(path=path)
    )
    return Tag(
        tag_id=t.get("tagId"),
        name=t["name"],
        type=t["type"],
        parameter=t.get("parameter"),
        firing_trigger_id=t.get("firingTriggerId", []),
        blocking_trigger_id=t.get("blockingTriggerId", []),
        paused=t.get("paused", False),
        notes=t.get("notes"),
    )


def create_tag(client: GTMClient, container_id: str, tag: Tag, workspace_id: str = "0") -> Tag:
    """Create a new tag in a workspace."""
    path = _workspace_path(client, container_id, workspace_id)
    body = tag.model_dump(exclude_none=True, exclude={"tag_id"})
    t = client.execute_with_retry(
        client.service.accounts().containers().workspaces().tags().create(parent=path, body=body)
    )
    return Tag(
        tag_id=t.get("tagId"),
        name=t["name"],
        type=t["type"],
        parameter=t.get("parameter"),
        firing_trigger_id=t.get("firingTriggerId", []),
        blocking_trigger_id=t.get("blockingTriggerId", []),
        paused=t.get("paused", False),
        notes=t.get("notes"),
    )


def update_tag(client: GTMClient, container_id: str, tag_id: str, tag: Tag, workspace_id: str = "0") -> Tag:
    """Update an existing tag."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/tags/{tag_id}"
    body = tag.model_dump(exclude_none=True, exclude={"tag_id"})
    t = client.execute_with_retry(
        client.service.accounts().containers().workspaces().tags().update(path=path, body=body)
    )
    return Tag(
        tag_id=t.get("tagId"),
        name=t["name"],
        type=t["type"],
        parameter=t.get("parameter"),
        firing_trigger_id=t.get("firingTriggerId", []),
        blocking_trigger_id=t.get("blockingTriggerId", []),
        paused=t.get("paused", False),
        notes=t.get("notes"),
    )


def delete_tag(client: GTMClient, container_id: str, tag_id: str, workspace_id: str = "0") -> None:
    """Delete a tag."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/tags/{tag_id}"
    client.execute_with_retry(
        client.service.accounts().containers().workspaces().tags().delete(path=path)
    )


def search_tags(client: GTMClient, container_id: str, query: str, workspace_id: str = "0") -> list[Tag]:
    """Search tags by name (case-insensitive substring match)."""
    all_tags = list_tags(client, container_id, workspace_id)
    query_lower = query.lower()
    return [t for t in all_tags if query_lower in t.name.lower()]
