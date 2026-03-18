"""Audit operations — naming compliance, unused items, consent checks, duplicate detection."""

import re

from gtm.client import GTMClient
from gtm.models import AuditFinding, AuditResult
from gtm.operations.containers import get_container
from gtm.operations.tags import list_tags
from gtm.operations.triggers import list_triggers
from gtm.operations.variables import list_variables


def audit_container(client: GTMClient, container_id: str, workspace_id: str = "0") -> AuditResult:
    """Run a full audit on a container workspace."""
    container = get_container(client, container_id)
    tags = list_tags(client, container_id, workspace_id)
    triggers = list_triggers(client, container_id, workspace_id)
    variables = list_variables(client, container_id, workspace_id)

    findings: list[AuditFinding] = []

    # Naming convention checks
    findings.extend(_check_naming(tags, "tag"))
    findings.extend(_check_naming(triggers, "trigger"))
    findings.extend(_check_naming(variables, "variable"))

    # Unused trigger detection
    findings.extend(_check_unused_triggers(tags, triggers))

    # Duplicate detection
    findings.extend(_check_duplicates(tags, "tag"))
    findings.extend(_check_duplicates(triggers, "trigger"))
    findings.extend(_check_duplicates(variables, "variable"))

    # Paused tag detection
    findings.extend(_check_paused_tags(tags))

    return AuditResult(
        container_id=container_id,
        container_name=container.name,
        findings=findings,
        tags_count=len(tags),
        triggers_count=len(triggers),
        variables_count=len(variables),
    )


def _check_naming(items: list, resource_type: str) -> list[AuditFinding]:
    """Check that names follow conventions (no leading/trailing spaces, reasonable length)."""
    findings = []
    for item in items:
        name = item.name
        if name != name.strip():
            findings.append(
                AuditFinding(
                    severity="warning",
                    category="naming",
                    resource_type=resource_type,
                    resource_name=name,
                    message="Name has leading or trailing whitespace",
                )
            )
        if len(name) > 100:
            findings.append(
                AuditFinding(
                    severity="warning",
                    category="naming",
                    resource_type=resource_type,
                    resource_name=name,
                    message=f"Name is very long ({len(name)} chars)",
                )
            )
        if re.search(r"[<>\"']", name):
            findings.append(
                AuditFinding(
                    severity="warning",
                    category="naming",
                    resource_type=resource_type,
                    resource_name=name,
                    message="Name contains special characters",
                )
            )
    return findings


def _check_unused_triggers(tags: list, triggers: list) -> list[AuditFinding]:
    """Find triggers that are not referenced by any tag."""
    used_trigger_ids = set()
    for tag in tags:
        used_trigger_ids.update(tag.firing_trigger_id)
        used_trigger_ids.update(tag.blocking_trigger_id)

    findings = []
    for trigger in triggers:
        if trigger.trigger_id and trigger.trigger_id not in used_trigger_ids:
            # Skip built-in triggers (All Pages, etc.)
            if trigger.type not in ("pageview", "domReady", "windowLoaded"):
                findings.append(
                    AuditFinding(
                        severity="info",
                        category="unused",
                        resource_type="trigger",
                        resource_name=trigger.name,
                        message="Trigger is not used by any tag",
                    )
                )
    return findings


def _check_duplicates(items: list, resource_type: str) -> list[AuditFinding]:
    """Find items with duplicate names."""
    name_counts: dict[str, int] = {}
    for item in items:
        name_counts[item.name] = name_counts.get(item.name, 0) + 1

    findings = []
    for name, count in name_counts.items():
        if count > 1:
            findings.append(
                AuditFinding(
                    severity="warning",
                    category="duplicate",
                    resource_type=resource_type,
                    resource_name=name,
                    message=f"Duplicate name found ({count} items)",
                )
            )
    return findings


def _check_paused_tags(tags: list) -> list[AuditFinding]:
    """Find paused tags that might be candidates for cleanup."""
    findings = []
    for tag in tags:
        if tag.paused:
            findings.append(
                AuditFinding(
                    severity="info",
                    category="unused",
                    resource_type="tag",
                    resource_name=tag.name,
                    message="Tag is paused — consider removing if no longer needed",
                )
            )
    return findings
