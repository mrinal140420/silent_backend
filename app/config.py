from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    MONGODB_ATLAS_URI: str
    APP_ENV: str = "development"
    JWT_SECRET: str | None = None


settings = Settings(
    MONGODB_ATLAS_URI=os.getenv("MONGODB_ATLAS_URI", ""),
    APP_ENV=os.getenv("APP_ENV", "development"),
    JWT_SECRET=os.getenv("JWT_SECRET"),
)

if not settings.MONGODB_ATLAS_URI:
    raise RuntimeError("MONGODB_ATLAS_URI is not set")
