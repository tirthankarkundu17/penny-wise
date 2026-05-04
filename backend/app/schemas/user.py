from pydantic import BaseModel, Field
from typing import Optional, Any


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: str
    password: str

class RefreshToken(BaseModel):
    refresh_token: str

class UserRead(UserBase):
    id: Any
    is_active: bool

    class Config:
        from_attributes = True
