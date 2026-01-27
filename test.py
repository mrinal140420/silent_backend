import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000/api"

# ---- Test file (already encrypted in real use) ----
TEST_FILE_PATH = "test_encrypted.bin"
Path(TEST_FILE_PATH).write_bytes(b"ENCRYPTED_TEST_DATA")

print("1️⃣ Testing /upload")

upload_resp = requests.post(
    f"{BASE_URL}/upload",
    files={"file": open(TEST_FILE_PATH, "rb")},
    data={
        "expires_in_hours": 1,
        "max_downloads": 1,
        "hash": "dummyhash123"
    }
)

assert upload_resp.status_code == 200, upload_resp.text
file_id = upload_resp.json()["file_id"]
print("   ✅ Uploaded, file_id:", file_id)

# --------------------------------------------------

print("\n2️⃣ Testing /create-link")

link_resp = requests.post(
    f"{BASE_URL}/create-link",
    params={
        "file_id": file_id,
        "expires_in_hours": 1
    }
)

assert link_resp.status_code == 200, link_resp.text
token = link_resp.json()["token"]
print("   ✅ Link created, token:", token)

# --------------------------------------------------

print("\n3️⃣ Testing /metadata")

meta_resp = requests.get(
    f"{BASE_URL}/file/{token}/metadata"
)

assert meta_resp.status_code == 200, meta_resp.text
print("   ✅ Metadata:", meta_resp.json())

# --------------------------------------------------

print("\n4️⃣ Testing /download (first download)")

download_resp = requests.get(
    f"{BASE_URL}/file/{token}/download"
)

assert download_resp.status_code == 200, download_resp.text
print("   ✅ Download succeeded")

# --------------------------------------------------

print("\n5️⃣ Testing /download again (should auto-destroy)")

download_resp_2 = requests.get(
    f"{BASE_URL}/file/{token}/download"
)

assert download_resp_2.status_code in (404, 410)
print("   ✅ File auto-destroyed after max downloads")

# --------------------------------------------------

print("\n6️⃣ Testing /metadata after destruction")

meta_resp_2 = requests.get(
    f"{BASE_URL}/file/{token}/metadata"
)

assert meta_resp_2.status_code == 404
print("   ✅ Metadata unavailable after destruction")


print("\n🎉 ALL TESTS PASSED SUCCESSFULLY")
