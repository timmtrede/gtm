"""Pydantic models for GTM resources."""

from pydantic import BaseModel


class Container(BaseModel):
    account_id: str
    container_id: str
    name: str
    public_id: str | None = None
    domain_name: list[str] = []
    notes: str | None = None
    usage_context: list[str] = []
    tag_manager_url: str | None = None

    @property
    def path(self) -> str:
        return f"accounts/{self.account_id}/containers/{self.container_id}"


class Tag(BaseModel):
    tag_id: str | None = None
    name: str
    type: str
    parameter: list[dict] | None = None
    firing_trigger_id: list[str] = []
    blocking_trigger_id: list[str] = []
    paused: bool = False
    notes: str | None = None


class Trigger(BaseModel):
    trigger_id: str | None = None
    name: str
    type: str
    filter: list[dict] | None = None
    custom_event_filter: list[dict] | None = None
    notes: str | None = None


class Variable(BaseModel):
    variable_id: str | None = None
    name: str
    type: str
    parameter: list[dict] | None = None
    notes: str | None = None


class Workspace(BaseModel):
    workspace_id: str | None = None
    name: str
    description: str | None = None


class Version(BaseModel):
    version_id: str | None = None
    name: str | None = None
    description: str | None = None
    container_id: str | None = None
    deleted: bool = False
    tag: list[dict] = []
    trigger: list[dict] = []
    variable: list[dict] = []


class AuditFinding(BaseModel):
    severity: str  # "error", "warning", "info"
    category: str  # "naming", "consent", "unused", "duplicate"
    resource_type: str  # "tag", "trigger", "variable"
    resource_name: str
    message: str


class AuditResult(BaseModel):
    container_id: str
    container_name: str
    findings: list[AuditFinding] = []
    tags_count: int = 0
    triggers_count: int = 0
    variables_count: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "warning")


class VersionDiff(BaseModel):
    version_a: str
    version_b: str
    added_tags: list[str] = []
    removed_tags: list[str] = []
    modified_tags: list[str] = []
    added_triggers: list[str] = []
    removed_triggers: list[str] = []
    modified_triggers: list[str] = []
    added_variables: list[str] = []
    removed_variables: list[str] = []
    modified_variables: list[str] = []
