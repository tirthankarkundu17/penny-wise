from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt", "bcrypt_sha256"], deprecated="auto"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # TODO: Implement refresh token creation logic
    # 1. Copy data
    # 2. Set expiration (usually much longer than access token)
    # 3. Set type to 'refresh'
    # 4. Encode and return
    pass


def decode_token(token: str) -> dict:
    # TODO: Implement token decoding and validation
    # 1. Use jwt.decode with settings.secret_key and settings.algorithm
    # 2. Handle JWTError and return appropriate info or raise HTTPException
    pass

