"""BigQuery operations — list datasets, tables, schemas, and run queries."""

from __future__ import annotations

from google.cloud import bigquery

from gtm.bigquery_client import BigQueryClient


def list_datasets(client: BigQueryClient) -> list[dict]:
    """List all datasets in the project."""
    return [
        {"dataset_id": ds.dataset_id, "project": ds.project}
        for ds in client.client.list_datasets()
    ]


def list_tables(client: BigQueryClient, dataset_id: str) -> list[dict]:
    """List all tables in a dataset."""
    dataset_ref = client.client.dataset(dataset_id)
    return [
        {"table_id": t.table_id, "table_type": t.table_type}
        for t in client.client.list_tables(dataset_ref)
    ]


def get_table_schema(client: BigQueryClient, dataset_id: str, table_id: str) -> dict:
    """Get schema and metadata for a table."""
    table_ref = f"{client.project}.{dataset_id}.{table_id}"
    table = client.client.get_table(table_ref)
    return {
        "table_id": table.table_id,
        "dataset_id": dataset_id,
        "table_type": table.table_type.name if hasattr(table.table_type, "name") else str(table.table_type),
        "num_rows": table.num_rows,
        "num_bytes": table.num_bytes,
        "created": table.created.isoformat() if table.created else None,
        "modified": table.modified.isoformat() if table.modified else None,
        "description": table.description,
        "schema": [
            {"name": f.name, "type": f.field_type, "mode": f.mode, "description": f.description}
            for f in table.schema
        ],
    }


def preview_table(client: BigQueryClient, dataset_id: str, table_id: str, limit: int = 10) -> list[dict]:
    """Preview rows from a table without running a query (uses list_rows API)."""
    table_ref = f"{client.project}.{dataset_id}.{table_id}"
    rows = client.client.list_rows(table_ref, max_results=limit)
    return [_row_to_dict(row) for row in rows]


def run_query(client: BigQueryClient, sql: str, limit: int = 100) -> dict:
    """Run a read-only SQL query and return results."""
    job_config = bigquery.QueryJobConfig(
        maximum_bytes_billed=10 * 1024 * 1024 * 1024,  # 10 GB safety limit
    )
    query_job = client.client.query(sql, job_config=job_config)
    results = query_job.result()

    rows = []
    for i, row in enumerate(results):
        if i >= limit:
            break
        rows.append(_row_to_dict(row))

    return {
        "rows": rows,
        "total_rows": results.total_rows,
        "bytes_processed": query_job.total_bytes_processed,
        "cache_hit": query_job.cache_hit,
    }


def dry_run_query(client: BigQueryClient, sql: str) -> dict:
    """Dry-run a query to estimate bytes processed without executing."""
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    query_job = client.client.query(sql, job_config=job_config)
    return {
        "total_bytes_processed": query_job.total_bytes_processed,
        "total_bytes_processed_human": _human_bytes(query_job.total_bytes_processed),
    }


def _row_to_dict(row) -> dict:
    """Convert a BigQuery row to a serializable dict."""
    data = dict(row)
    for key, val in data.items():
        if hasattr(val, "isoformat"):
            data[key] = val.isoformat()
        elif isinstance(val, bytes):
            data[key] = val.decode("utf-8", errors="replace")
    return data


def _human_bytes(n: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"
