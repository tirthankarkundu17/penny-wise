from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime


class ItemBase(BaseModel):
    hsn: Optional[str] = None
    item_name: str
    description: Optional[str] = None
    net_price: float
    qty: float
    value: float


class ItemRead(ItemBase):
    id: Any
    bill_id: Any

    class Config:
        from_attributes = True


class BillBase(BaseModel):
    store_name: str
    bill_date: str
    bill_number: Optional[str] = None
    grand_total: float


class BillCreate(BillBase):
    items: List[ItemBase]


class BillRead(BillBase):
    id: Any
    user_id: Optional[Any]
    created_at: datetime
    items: List[ItemRead]

    class Config:
        from_attributes = True


class PriceHistory(BaseModel):
    date: str
    price: float
    store: str
    bill_date: str
    bill_number: Optional[str] = None
    item_name: str
    item_description: Optional[str] = None
