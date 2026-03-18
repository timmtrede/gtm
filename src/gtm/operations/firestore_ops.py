"""Firestore operations — query events, customers, scores, domains."""

from __future__ import annotations

from google.cloud.firestore_v1 import FieldFilter

from gtm.firestore_client import FirestoreClient


def list_collections(client: FirestoreClient) -> list[dict]:
    """List all root collections with document counts."""
    results = []
    for col in client.db.collections():
        count_result = col.count().get()
        count = count_result[0][0].value if count_result and count_result[0] else 0
        results.append({"name": col.id, "document_count": count})
    return results


def query_events(
    client: FirestoreClient,
    event_name: str | None = None,
    user_id: str | None = None,
    transaction_id: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Query the zipmend events collection with optional filters."""
    col = client.db.collection("zipmend")
    query = col

    if event_name:
        query = query.where(filter=FieldFilter("event_name", "==", event_name))
    if user_id:
        query = query.where(filter=FieldFilter("user_id", "==", user_id))
    if transaction_id:
        query = query.where(filter=FieldFilter("transaction_id", "==", transaction_id))

    query = query.limit(limit)
    return [_doc_to_dict(doc) for doc in query.stream()]


def get_event(client: FirestoreClient, doc_id: str) -> dict | None:
    """Get a single event document by ID."""
    doc = client.db.collection("zipmend").document(doc_id).get()
    if doc.exists:
        return _doc_to_dict(doc)
    return None


def list_customers(client: FirestoreClient, limit: int = 50) -> list[dict]:
    """List existing customers."""
    col = client.db.collection("existing_customers")
    return [_doc_to_dict(doc) for doc in col.limit(limit).stream()]


def lookup_customer(client: FirestoreClient, user_id: str) -> list[dict]:
    """Find customer records by user_id."""
    col = client.db.collection("existing_customers")
    query = col.where(filter=FieldFilter("user_id", "==", user_id))
    return [_doc_to_dict(doc) for doc in query.stream()]


def get_score(client: FirestoreClient, domain: str) -> dict | None:
    """Get the score document for a domain."""
    doc = client.db.collection("scores").document(domain).get()
    if doc.exists:
        return _doc_to_dict(doc)
    return None


def query_scores(client: FirestoreClient, limit: int = 20) -> list[dict]:
    """List score documents."""
    col = client.db.collection("scores")
    return [_doc_to_dict(doc) for doc in col.limit(limit).stream()]


def is_generic_domain(client: FirestoreClient, domain: str) -> bool:
    """Check if a domain is in the generic domains list."""
    doc = client.db.collection("generic_domains").document(domain).get()
    return doc.exists


def list_generic_domains(client: FirestoreClient, limit: int = 50) -> list[str]:
    """List generic email domains."""
    col = client.db.collection("generic_domains")
    return [doc.id for doc in col.limit(limit).stream()]


def query_collection(
    client: FirestoreClient,
    collection: str,
    field: str | None = None,
    op: str = "==",
    value: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Generic query on any collection."""
    col = client.db.collection(collection)
    query = col

    if field and value:
        query = query.where(filter=FieldFilter(field, op, value))

    query = query.limit(limit)
    return [_doc_to_dict(doc) for doc in query.stream()]


def _doc_to_dict(doc) -> dict:
    """Convert a Firestore document to a serializable dict."""
    data = doc.to_dict()
    data["_id"] = doc.id
    # Convert non-serializable types
    for key, val in data.items():
        if hasattr(val, "isoformat"):
            data[key] = val.isoformat()
    return data
