from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, Any
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)

    bills: List["Bill"] = Relationship(back_populates="user")


class Item(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    bill_id: Optional[str] = Field(default=None, foreign_key="bill.id")
    hsn: Optional[str] = None
    item_name: str
    description: Optional[str] = None
    net_price: float
    qty: float
    value: float
    category: Optional[str] = None

    bill: "Bill" = Relationship(back_populates="items")


class Bill(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="user.id")
    store_name: str
    bill_date: str  # Storing as string as provided by Gemini, can be converted later
    bill_number: Optional[str] = None
    grand_total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="bills")
    items: List[Item] = Relationship(back_populates="bill")
