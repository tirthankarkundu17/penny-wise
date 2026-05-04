from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.db.repositories import get_repository
from app.db.repositories.base import BaseRepository
from app.models.user import User
from app.schemas.token import TokenData
from app.core import security  # Import the security module

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: BaseRepository = Depends(get_repository),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Refactor to use security.decode_token for consistency
        payload = security.decode_token(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await repo.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user
