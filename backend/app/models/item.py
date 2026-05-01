from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.bill import Bill


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
