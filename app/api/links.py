from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta

from ..db.mongo import files_col, access_links_col
from ..utils.security import generate_token, hash_password

router = APIRouter()


@router.post("/create-link")
def create_link(file_id: str, expires_in_hours: int, password: str | None = None):
    file = files_col.find_one({"file_id": file_id})
    if not file or file["destroyed"]:
        raise HTTPException(status_code=404, detail="File not found")

    token = generate_token()
    now = datetime.utcnow()

    access_links_col.insert_one({
        "token": token,
        "file_id": file_id,
        "expires_at": now + timedelta(hours=expires_in_hours),
        "password_hash": hash_password(password) if password else None,
        "revoked": False
    })

    return {"token": token}
