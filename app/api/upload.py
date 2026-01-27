from fastapi import APIRouter, UploadFile, File, Form, Request, HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from ..db.mongo import files_col
from ..services.gridfs import save_encrypted_file
from ..services.rate_limit import allow_ip

router = APIRouter()

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100 MB (Render-safe)


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    expires_in_hours: int = Form(...),
    max_downloads: int = Form(...),
    hash: str = Form(...)
):
    # -------------------------
    # Rate limiting (EARLY)
    # -------------------------
    ip = request.client.host if request.client else "unknown"
    if not allow_ip(ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # -------------------------
    # Read file into memory
    # -------------------------
    data = await file.read()

    # -------------------------
    # Size enforcement (CRITICAL)
    # -------------------------
    if len(data) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large (max 100 MB)"
        )

    # -------------------------
    # Save encrypted file
    # -------------------------
    gridfs_id = save_encrypted_file(data, file.filename)

    # -------------------------
    # Metadata persistence
    # -------------------------
    file_id = str(uuid4())
    now = datetime.utcnow()

    files_col.insert_one({
        "file_id": file_id,
        "filename": file.filename,
        "size_bytes": len(data),
        "hash": hash,
        "created_at": now,
        "expires_at": now + timedelta(hours=expires_in_hours),
        "max_downloads": max_downloads,
        "download_count": 0,
        "destroyed": False,
        "gridfs_id": gridfs_id
    })

    return {"file_id": file_id}
