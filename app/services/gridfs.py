from ..db.mongo import fs


def save_encrypted_file(data: bytes, filename: str) -> str:
    return fs.put(data, filename=filename)


def get_encrypted_file(file_ref):
    return fs.get(file_ref)


def delete_file(file_ref):
    fs.delete(file_ref)
