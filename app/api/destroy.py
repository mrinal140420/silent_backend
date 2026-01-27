from fastapi import APIRouter, HTTPException
from ..services.cleanup import destroy_file
from ..db.mongo import files_col

router = APIRouter()


@router.post("/file/{file_id}/destroy")
def destroy(file_id: str):
    file = files_col.find_one({"file_id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    destroy_file(file_id)
    return {"status": "destroyed"}
