"""JSON diff utilities for version comparison."""

from deepdiff import DeepDiff


def diff_json(a: dict, b: dict) -> dict:
    """Return a structured diff between two JSON objects."""
    return DeepDiff(a, b, ignore_order=True).to_dict()


def format_diff_summary(diff: dict) -> str:
    """Format a DeepDiff result as a human-readable summary."""
    lines = []
    if "dictionary_item_added" in diff:
        lines.append(f"Added: {len(diff['dictionary_item_added'])} items")
    if "dictionary_item_removed" in diff:
        lines.append(f"Removed: {len(diff['dictionary_item_removed'])} items")
    if "values_changed" in diff:
        lines.append(f"Changed: {len(diff['values_changed'])} values")
    if "iterable_item_added" in diff:
        lines.append(f"List items added: {len(diff['iterable_item_added'])}")
    if "iterable_item_removed" in diff:
        lines.append(f"List items removed: {len(diff['iterable_item_removed'])}")
    return "\n".join(lines) if lines else "No differences found"
