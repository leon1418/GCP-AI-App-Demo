import logging

import firebase_admin
from firebase_admin import auth as firebase_auth
from fastapi import FastAPI, File, Header, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.models import HealthResponse, HistoryResponse, HistoryItem, UploadResponse
from app.services import firestore_service, gcs_service, gemini_service

logger = logging.getLogger(__name__)

firebase_admin.initialize_app()

app = FastAPI(title="Dog Breed Detector")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def _get_user_id(authorization: str | None) -> str | None:
    """Verify Firebase ID token and return user ID."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    try:
        decoded = firebase_auth.verify_id_token(token)
        return decoded["uid"]
    except Exception:
        return None


@app.post("/api/upload", response_model=UploadResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    authorization: str | None = Header(None),
):
    user_id = _get_user_id(authorization)
    if not user_id:
        return JSONResponse(status_code=401, content={"detail": "Authentication required"})

    extension = file.filename.rsplit(".", 1)[-1].lower() if file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        return JSONResponse(
            status_code=400,
            content={"detail": f"File type not allowed. Use: {', '.join(ALLOWED_EXTENSIONS)}"},
        )

    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        return JSONResponse(status_code=400, content={"detail": "File too large. Max 10MB."})

    try:
        gcs_uri, public_url = gcs_service.upload_image(content, user_id, extension)
        results = gemini_service.analyze_image(gcs_uri)
        query_id = firestore_service.save_query(user_id, public_url, gcs_uri, results)
    except Exception as e:
        logger.exception("Upload processing failed")
        return JSONResponse(status_code=500, content={"detail": str(e)})

    return UploadResponse(query_id=query_id, image_url=public_url, results=results)


@app.get("/api/history", response_model=HistoryResponse)
async def get_history(authorization: str | None = Header(None), limit: int = 20):
    user_id = _get_user_id(authorization)
    if not user_id:
        return JSONResponse(status_code=401, content={"detail": "Authentication required"})

    items = firestore_service.get_user_history(user_id, limit=min(limit, 50))
    return HistoryResponse(
        items=[
            HistoryItem(
                query_id=item["query_id"],
                image_url=item["image_url"],
                results=item["results"],
                timestamp=item["timestamp"],
            )
            for item in items
        ]
    )


@app.delete("/api/history/{query_id}")
async def delete_history_item(query_id: str, authorization: str | None = Header(None)):
    user_id = _get_user_id(authorization)
    if not user_id:
        return JSONResponse(status_code=401, content={"detail": "Authentication required"})

    deleted = firestore_service.delete_query(query_id, user_id)
    if not deleted:
        return JSONResponse(status_code=404, content={"detail": "Query not found"})
    return {"deleted": True}


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse()


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
