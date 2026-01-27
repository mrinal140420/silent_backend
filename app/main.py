from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import destroy, download, links, upload , metadata


app = FastAPI(
    title="SilentDrop Backend",
    description="Zero-knowledge encrypted file transfer backend",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(links.router, prefix="/api")
app.include_router(download.router, prefix="/api")
app.include_router(destroy.router, prefix="/api")
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "SilentDrop Backend",
        "zero_knowledge": True
    }
app.include_router(metadata.router, prefix="/api")
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"

    return response
