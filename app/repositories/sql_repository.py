from typing import List, Optional, Any
from sqlmodel import Session, select
from app.models import User, Bill, Item
from app.schemas import UserCreate
from app.repositories.base import BaseRepository


class SQLRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return self.session.exec(select(User).where(User.username == username)).first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.exec(select(User).where(User.email == email)).first()

    async def create_bill(self, user_id: Any, extracted_data: Any) -> Bill:
        db_bill = Bill(
            user_id=user_id,
            store_name=extracted_data.store_name,
            bill_date=extracted_data.bill_date,
            bill_number=extracted_data.bill_number,
            grand_total=extracted_data.grand_total,
        )
        self.session.add(db_bill)
        self.session.commit()
        self.session.refresh(db_bill)

        for item_data in extracted_data.items:
            db_item = Item(
                bill_id=db_bill.id,
                hsn=item_data.hsn,
                item_name=item_data.item_name,
                description=item_data.description,
                net_price=item_data.net_price,
                qty=item_data.qty,
                value=item_data.value,
            )
            self.session.add(db_item)

        self.session.commit()
        self.session.refresh(db_bill)
        return db_bill

    async def get_bills_by_user(self, user_id: Any) -> List[Bill]:
        return self.session.exec(select(Bill).where(Bill.user_id == user_id)).all()

    async def get_price_history(self, user_id: Any, item_name: str) -> List[Any]:
        statement = (
            select(Item, Bill)
            .join(Bill)
            .where(Bill.user_id == user_id)
            .where(
                (Item.item_name.ilike(f"%{item_name}%"))
                | (Item.description.ilike(f"%{item_name}%"))
            )
            .order_by(Bill.bill_date)
        )
        return self.session.exec(statement).all()
