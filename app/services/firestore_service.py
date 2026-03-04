import uuid
from datetime import datetime, timezone

from google.cloud import firestore

from app.config import settings
from app.models import AnalysisResults


def get_client() -> firestore.Client:
    return firestore.Client(project=settings.gcp_project_id)


def save_query(
    user_id: str,
    image_url: str,
    gcs_uri: str,
    results: AnalysisResults,
) -> str:
    """Save query results to Firestore. Returns query_id."""
    client = get_client()
    query_id = f"q_{uuid.uuid4().hex[:12]}"

    doc_ref = client.collection("queries").document(query_id)
    doc_ref.set({
        "query_id": query_id,
        "user_id": user_id,
        "image_url": image_url,
        "gcs_uri": gcs_uri,
        "results": results.model_dump(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    return query_id


def get_user_history(user_id: str, limit: int = 20) -> list[dict]:
    """Get query history for a session, ordered by most recent first."""
    client = get_client()

    docs = (
        client.collection("queries")
        .where("user_id", "==", user_id)
        .order_by("timestamp", direction=firestore.Query.DESCENDING)
        .limit(limit)
        .stream()
    )

    return [doc.to_dict() for doc in docs]


def delete_query(query_id: str, user_id: str) -> bool:
    """Delete a query if it belongs to the session. Returns True if deleted."""
    client = get_client()
    doc_ref = client.collection("queries").document(query_id)
    doc = doc_ref.get()
    if not doc.exists or doc.to_dict().get("user_id") != user_id:
        return False
    doc_ref.delete()
    return True
