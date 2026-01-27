from passlib.context import CryptContext
import secrets

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)
