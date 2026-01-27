from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.db.mongo import files_col, access_links_col

router = APIRouter()


@router.get("/file/{token}/metadata")
def get_file_metadata(token: str):
    # Validate access link
    link = access_links_col.find_one(
        {"token": token, "revoked": False}
    )

    if not link:
        raise HTTPException(status_code=404, detail="Invalid or expired link")

    # Fetch file metadata
    file = files_col.find_one(
        {"file_id": link["file_id"], "destroyed": False}
    )

    if not file:
        raise HTTPException(status_code=410, detail="File no longer exists")

    # Enforce expiry
    if file["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=410, detail="File expired")

    remaining_downloads = max(
        0,
        file["max_downloads"] - file["download_count"]
    )

    return {
        "filename": file["filename"],
        "size_bytes": file["size_bytes"],
        "created_at": file["created_at"],
        "expires_at": file["expires_at"],
        "remaining_downloads": remaining_downloads,
    }
