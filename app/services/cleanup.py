from app.db.mongo import files_col, access_links_col, fs


def destroy_file(file_id: str):
    """
    Permanently deletes:
    - encrypted file from GridFS
    - file metadata
    - all access links
    """
    file = files_col.find_one({"file_id": file_id})
    if not file:
        return

    # Delete encrypted file
    if "gridfs_id" in file:
        try:
            fs.delete(file["gridfs_id"])
        except Exception:
            pass  # file may already be gone

    # Delete metadata & links
    files_col.delete_one({"file_id": file_id})
    access_links_col.delete_many({"file_id": file_id})
