from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Header
from fastapi.responses import StreamingResponse

from app.db.mongo import files_col, access_links_col, fs
from app.utils.security import verify_password
from app.services.cleanup import destroy_file
from app.services.rate_limit import allow_ip, allow_token

router = APIRouter()


@router.get("/file/{token}/download")
def download_file(
    token: str,
    request: Request,
    background_tasks: BackgroundTasks,
    x_file_password: str | None = Header(default=None)
):
    # -------------------------
    # Rate limiting (EARLY EXIT)
    # -------------------------
    ip = request.client.host if request.client else "unknown"

    if not allow_ip(ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests from this IP"
        )

    if not allow_token(token):
        raise HTTPException(
            status_code=429,
            detail="Too many requests for this link"
        )

    # -------------------------
    # Access link validation
    # -------------------------
    link = access_links_col.find_one({
        "token": token,
        "revoked": False
    })

    if not link:
        raise HTTPException(
            status_code=404,
            detail="Invalid link"
        )

    file = files_col.find_one({
        "file_id": link["file_id"],
        "destroyed": False
    })

    if not file:
        raise HTTPException(
            status_code=410,
            detail="File destroyed"
        )

    # -------------------------
    # Password enforcement (HASHED)
    # -------------------------
    if link.get("password_hash"):
        if not x_file_password:
            raise HTTPException(
                status_code=401,
                detail="Password required"
            )

        if not verify_password(
            x_file_password,
            link["password_hash"]
        ):
            raise HTTPException(
                status_code=403,
                detail="Invalid password"
            )

    # -------------------------
    # Download limit enforcement
    # -------------------------
    if file["download_count"] >= file["max_downloads"]:
        destroy_file(file["file_id"])
        raise HTTPException(
            status_code=410,
            detail="File expired"
        )

    # -------------------------
    # Fetch GridFS file FIRST
    # -------------------------
    try:
        grid_file = fs.get(file["gridfs_id"])
    except Exception:
        raise HTTPException(
            status_code=410,
            detail="File no longer exists"
        )

    # -------------------------
    # Increment download count
    # -------------------------
    updated = files_col.find_one_and_update(
        {"file_id": file["file_id"]},
        {"$inc": {"download_count": 1}},
        return_document=True
    )

    # If last allowed download → destroy AFTER response
    if updated["download_count"] >= updated["max_downloads"]:
        background_tasks.add_task(
            destroy_file,
            updated["file_id"]
        )

    # -------------------------
    # Stream file
    # -------------------------
    return StreamingResponse(
        grid_file,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{file["filename"]}"'
            )
        }
    )

