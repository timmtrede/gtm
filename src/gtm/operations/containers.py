"""Container operations — list, get, export."""

import json
from pathlib import Path

from gtm.client import GTMClient
from gtm.models import Container


def list_containers(client: GTMClient) -> list[Container]:
    """List all containers in the account."""
    result = client.execute_with_retry(
        client.service.accounts().containers().list(parent=client.account_path)
    )
    containers = []
    for c in result.get("container", []):
        containers.append(
            Container(
                account_id=client.account_id,
                container_id=c["containerId"],
                name=c["name"],
                public_id=c.get("publicId"),
                domain_name=c.get("domainName", []),
                notes=c.get("notes"),
                usage_context=c.get("usageContext", []),
                tag_manager_url=c.get("tagManagerUrl"),
            )
        )
    return containers


def get_container(client: GTMClient, container_id: str) -> Container:
    """Get a single container by ID."""
    path = f"{client.account_path}/containers/{container_id}"
    c = client.execute_with_retry(
        client.service.accounts().containers().get(path=path)
    )
    return Container(
        account_id=client.account_id,
        container_id=c["containerId"],
        name=c["name"],
        public_id=c.get("publicId"),
        domain_name=c.get("domainName", []),
        notes=c.get("notes"),
        usage_context=c.get("usageContext", []),
        tag_manager_url=c.get("tagManagerUrl"),
    )


def export_container(client: GTMClient, container_id: str, output_dir: Path | None = None) -> Path:
    """Export the live container version as JSON."""
    from gtm.operations.versions import get_live_version

    version = get_live_version(client, container_id)
    if output_dir is None:
        output_dir = Path("backups") / container_id

    output_dir.mkdir(parents=True, exist_ok=True)
    version_id = version.get("containerVersionId", "unknown")
    filename = output_dir / f"v{version_id}.json"
    filename.write_text(json.dumps(version, indent=2, ensure_ascii=False))
    return filename
