import uuid
from datetime import datetime, timezone

from google.cloud import storage

from app.config import settings


def get_client() -> storage.Client:
    return storage.Client(project=settings.gcp_project_id)


def upload_image(file_content: bytes, session_id: str, extension: str) -> tuple[str, str]:
    """Upload image to GCS and return (gcs_uri, public_url)."""
    client = get_client()
    bucket = client.bucket(settings.gcs_bucket_name)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    blob_name = f"uploads/{session_id}/{timestamp}_{unique_id}.{extension}"

    blob = bucket.blob(blob_name)
    content_type = f"image/{extension}" if extension != "jpg" else "image/jpeg"
    blob.upload_from_string(file_content, content_type=content_type)

    gcs_uri = f"gs://{settings.gcs_bucket_name}/{blob_name}"
    public_url = f"https://storage.googleapis.com/{settings.gcs_bucket_name}/{blob_name}"

    return gcs_uri, public_url
