"""Container export utilities."""

import json
from datetime import datetime, timezone
from pathlib import Path


def export_to_file(data: dict, container_id: str, version_id: str, output_dir: Path | None = None) -> Path:
    """Export container data to a JSON file in the backups directory."""
    if output_dir is None:
        output_dir = Path("backups") / container_id

    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(tz=timezone.utc).strftime("%Y%m%d")
    filename = output_dir / f"{date_str}_v{version_id}.json"
    filename.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return filename
