from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from typing import List, Optional
from datetime import datetime

from app.models.user import User
from app.models.item import Item


class Bill(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("bill_number", "store_name", name="uq_bill_number_store"),
    )
    id: Optional[str] = Field(default=None, primary_key=True)
    user_id: Optional[str] = Field(default=None, foreign_key="user.id")
    store_name: str
    bill_date: str
    bill_number: Optional[str] = None
    grand_total: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="bills")
    items: List[Item] = Relationship(back_populates="bill")
