from datetime import datetime
from typing import Any, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.repositories.base import BaseRepository
from app.models.bill import Bill
from app.models.item import Item
from app.models.user import User
from app.schemas.bill import BillCreate
from app.schemas.user import UserCreate


class MongoDBRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db

    async def create_user(self, user: UserCreate, hashed_password: str) -> User:
        doc = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password,
            "full_name": user.full_name,
            "is_active": True,
            "created_at": datetime.utcnow(),
        }
        result = await self.db.users.insert_one(doc)
        doc["id"] = str(result.inserted_id)
        return User(**doc)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        doc = await self.db.users.find_one({"username": username})
        if doc:
            doc["id"] = str(doc.pop("_id"))
            return User(**doc)
        return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        doc = await self.db.users.find_one({"email": email})
        if doc:
            doc["id"] = str(doc.pop("_id"))
            return User(**doc)
        return None

    async def create_bill(self, user_id: Any, extracted_data: BillCreate) -> Bill:
        doc = {
            "user_id": str(user_id),
            "store_name": extracted_data.store_name,
            "bill_date": extracted_data.bill_date,
            "bill_number": extracted_data.bill_number,
            "grand_total": extracted_data.grand_total,
            "created_at": datetime.utcnow(),
            "items": [item.model_dump() for item in extracted_data.items],
        }
        result = await self.db.bills.insert_one(doc)
        bill_id = str(result.inserted_id)
        doc["id"] = bill_id

        items = [
            Item(**{**item_data, "id": i, "bill_id": bill_id})
            for i, item_data in enumerate(doc["items"])
        ]
        doc.pop("items")
        bill = Bill(**doc)
        bill.items = items
        return bill

    async def get_bills_by_user(self, user_id: Any) -> List[Bill]:
        cursor = self.db.bills.find({"user_id": str(user_id)})
        docs = await cursor.to_list(length=100)
        bills = []
        for doc in docs:
            doc["id"] = str(doc.pop("_id"))
            items_data = doc.pop("items", [])
            items = [
                Item(**{**item, "id": i, "bill_id": doc["id"]})
                for i, item in enumerate(items_data)
            ]
            bill = Bill(**doc)
            bill.items = items
            bills.append(bill)
        return bills

    async def get_price_history(self, user_id: Any, item_name: str) -> List[Any]:
        pipeline = [
            {"$match": {"user_id": str(user_id)}},
            {"$unwind": "$items"},
            {
                "$match": {
                    "$or": [
                        {"items.item_name": {"$regex": item_name, "$options": "i"}},
                        {"items.description": {"$regex": item_name, "$options": "i"}},
                    ]
                }
            },
            {"$sort": {"bill_date": 1}},
        ]
        results = await self.db.bills.aggregate(pipeline).to_list(length=100)

        history = []
        for r in results:
            item_data = r["items"]
            item_data.update({"id": 0, "bill_id": str(r["_id"])})
            item = Item(**item_data)
            r["id"] = str(r.pop("_id"))
            r.pop("items")
            bill = Bill(**r)
            history.append((item, bill))
        return history
