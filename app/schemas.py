from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: Any
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ItemBase(BaseModel):
    hsn: Optional[str] = None
    item_name: str
    description: Optional[str] = None
    net_price: float
    qty: float
    value: float


class BillBase(BaseModel):
    store_name: str
    bill_date: str
    bill_number: Optional[str] = None
    grand_total: float


class BillCreate(BillBase):
    items: List[ItemBase]


class ItemRead(ItemBase):
    id: Any
    bill_id: Any


class BillRead(BillBase):
    id: Any
    user_id: Optional[Any]
    created_at: datetime
    items: List[ItemRead]


class PriceHistory(BaseModel):
    date: str
    price: float
    store: str
    bill_date: str
    bill_number: Optional[str] = None
    item_name: str
    item_description: Optional[str] = None
    
