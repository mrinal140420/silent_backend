from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from gridfs import GridFS
from app.config import settings

client = MongoClient(settings.MONGODB_ATLAS_URI)
db = client["silentdrop"]

try:
    client.admin.command("ping")
except ConnectionFailure:
    raise RuntimeError("MongoDB connection failed")

# Collections
files_col = db["files"]
access_links_col = db["access_links"]
access_logs_col = db["access_logs"]

# GridFS
fs = GridFS(db)


def init_indexes():
    files_col.create_index("file_id", unique=True)
    files_col.create_index("expires_at", expireAfterSeconds=0)

    access_links_col.create_index("token", unique=True)
    access_links_col.create_index("expires_at", expireAfterSeconds=0)


init_indexes()
