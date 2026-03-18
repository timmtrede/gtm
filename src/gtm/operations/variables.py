"""Variable operations — CRUD."""

from gtm.client import GTMClient
from gtm.models import Variable


def _workspace_path(client: GTMClient, container_id: str, workspace_id: str = "0") -> str:
    return f"{client.account_path}/containers/{container_id}/workspaces/{workspace_id}"


def list_variables(client: GTMClient, container_id: str, workspace_id: str = "0") -> list[Variable]:
    """List all variables in a workspace."""
    path = _workspace_path(client, container_id, workspace_id)
    result = client.execute_with_retry(
        client.service.accounts().containers().workspaces().variables().list(parent=path)
    )
    return [
        Variable(
            variable_id=v.get("variableId"),
            name=v["name"],
            type=v["type"],
            parameter=v.get("parameter"),
            notes=v.get("notes"),
        )
        for v in result.get("variable", [])
    ]


def get_variable(client: GTMClient, container_id: str, variable_id: str, workspace_id: str = "0") -> Variable:
    """Get a single variable by ID."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/variables/{variable_id}"
    v = client.execute_with_retry(
        client.service.accounts().containers().workspaces().variables().get(path=path)
    )
    return Variable(
        variable_id=v.get("variableId"),
        name=v["name"],
        type=v["type"],
        parameter=v.get("parameter"),
        notes=v.get("notes"),
    )


def create_variable(client: GTMClient, container_id: str, variable: Variable, workspace_id: str = "0") -> Variable:
    """Create a new variable."""
    path = _workspace_path(client, container_id, workspace_id)
    body = variable.model_dump(exclude_none=True, exclude={"variable_id"})
    v = client.execute_with_retry(
        client.service.accounts().containers().workspaces().variables().create(parent=path, body=body)
    )
    return Variable(
        variable_id=v.get("variableId"),
        name=v["name"],
        type=v["type"],
        parameter=v.get("parameter"),
        notes=v.get("notes"),
    )


def update_variable(
    client: GTMClient, container_id: str, variable_id: str, variable: Variable, workspace_id: str = "0"
) -> Variable:
    """Update an existing variable."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/variables/{variable_id}"
    body = variable.model_dump(exclude_none=True, exclude={"variable_id"})
    v = client.execute_with_retry(
        client.service.accounts().containers().workspaces().variables().update(path=path, body=body)
    )
    return Variable(
        variable_id=v.get("variableId"),
        name=v["name"],
        type=v["type"],
        parameter=v.get("parameter"),
        notes=v.get("notes"),
    )


def delete_variable(client: GTMClient, container_id: str, variable_id: str, workspace_id: str = "0") -> None:
    """Delete a variable."""
    path = f"{_workspace_path(client, container_id, workspace_id)}/variables/{variable_id}"
    client.execute_with_retry(
        client.service.accounts().containers().workspaces().variables().delete(path=path)
    )
