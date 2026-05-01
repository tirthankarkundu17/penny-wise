from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bill_id: Optional[int] = Field(default=None, foreign_key="bill.id")
    hsn: Optional[str] = None
    item_name: str
    description: Optional[str] = None
    net_price: float
    qty: float
    value: float
    category: Optional[str] = None

    bill: "Bill" = Relationship(back_populates="items")


class Bill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    store_name: str
    bill_date: str  # Storing as string as provided by Gemini, can be converted later
    bill_number: Optional[str] = None
    grand_total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    items: List[Item] = Relationship(back_populates="bill")
