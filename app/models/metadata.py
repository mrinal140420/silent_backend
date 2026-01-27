from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class FileMetadata(BaseModel):
    file_id: UUID
    filename: str
    size_bytes: int
    hash: str
    created_at: datetime
    expires_at: datetime
    max_downloads: int
    download_count: int = 0
    destroyed: bool = False
