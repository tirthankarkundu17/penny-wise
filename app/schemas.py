from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    id: int
    bill_id: int

class BillRead(BillBase):
    id: int
    created_at: datetime
    items: List[ItemRead]

class PriceHistory(BaseModel):
    date: str
    price: float
    store: str
