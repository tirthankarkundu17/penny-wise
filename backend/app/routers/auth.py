from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.db.repositories import get_repository
from app.db.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserRead, UserLogin
from app.schemas.token import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    repo: BaseRepository = Depends(get_repository),
) -> UserRead:
    existing = await repo.get_user_by_username(
        user.username
    ) or await repo.get_user_by_email(user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )
    hashed = get_password_hash(user.password)
    return await repo.create_user(user, hashed)


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    repo: BaseRepository = Depends(get_repository),
) -> Token:
    user = await repo.get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    repo: BaseRepository = Depends(get_repository),
) -> Token:
    # Decode and validate the refresh token using decode_token
    payload = decode_token(refresh_token)

    if payload.get("token_type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # (Optional but recommended) Check if the refresh token is in the database/allowlist
    existing_token = await repo.get_refresh_token_by_value(refresh_token)
    if not existing_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Get the user from the database
    user = await repo.get_user_by_username(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create a new access token
    access_token = create_access_token(data={"sub": user.username})
    # (Optional) Rotate the refresh token (create a new refresh token and revoke the old one)
    new_refresh_token = create_refresh_token(data={"sub": user.username})
    await repo.update_refresh_token(refresh_token, new_refresh_token)

    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )
