"""Tests for Pydantic models."""

from gtm.models import AuditFinding, AuditResult, Container, Tag, Trigger, Variable, VersionDiff


def test_container_path():
    c = Container(account_id="123", container_id="456", name="Test")
    assert c.path == "accounts/123/containers/456"


def test_tag_defaults():
    t = Tag(name="Test Tag", type="html")
    assert t.paused is False
    assert t.firing_trigger_id == []
    assert t.tag_id is None


def test_trigger_defaults():
    t = Trigger(name="Test Trigger", type="pageview")
    assert t.trigger_id is None
    assert t.filter is None


def test_variable_defaults():
    v = Variable(name="Test Var", type="v")
    assert v.variable_id is None
    assert v.parameter is None


def test_audit_result_counts():
    result = AuditResult(
        container_id="123",
        container_name="Test",
        findings=[
            AuditFinding(severity="error", category="naming", resource_type="tag", resource_name="t1", message="bad"),
            AuditFinding(severity="warning", category="unused", resource_type="trigger", resource_name="t2", message="unused"),
            AuditFinding(severity="warning", category="duplicate", resource_type="tag", resource_name="t3", message="dup"),
            AuditFinding(severity="info", category="unused", resource_type="tag", resource_name="t4", message="paused"),
        ],
    )
    assert result.error_count == 1
    assert result.warning_count == 2


def test_version_diff_defaults():
    d = VersionDiff(version_a="1", version_b="2")
    assert d.added_tags == []
    assert d.modified_triggers == []
