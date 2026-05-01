import asyncio
from typing import List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models import User, Bill, Item
from app.schemas import UserCreate
from app.repositories.base import BaseRepository
from datetime import datetime


class MongoDBRepository(BaseRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user_dict = {
            "username": user.username,
            "email": user.email,
            "hashed_password": hashed_password,
            "full_name": user.full_name,
            "is_active": True,
            "created_at": datetime.utcnow(),
        }
        result = await self.db.users.insert_one(db_user_dict)
        db_user_dict["id"] = str(result.inserted_id)
        return User(**db_user_dict)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user_dict = await self.db.users.find_one({"username": username})
        if user_dict:
            user_dict["id"] = str(user_dict.pop("_id"))
            return User(**user_dict)
        return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user_dict = await self.db.users.find_one({"email": email})
        if user_dict:
            user_dict["id"] = str(user_dict.pop("_id"))
            return User(**user_dict)
        return None

    async def create_bill(self, user_id: Any, extracted_data: Any) -> Bill:
        bill_dict = {
            "user_id": str(user_id),
            "store_name": extracted_data.store_name,
            "bill_date": extracted_data.bill_date,
            "bill_number": extracted_data.bill_number,
            "grand_total": extracted_data.grand_total,
            "created_at": datetime.utcnow(),
            "items": [item.dict() for item in extracted_data.items],
        }
        result = await self.db.bills.insert_one(bill_dict)
        bill_dict["id"] = str(result.inserted_id)

        # Format items for return
        items = []
        for i, item_data in enumerate(bill_dict["items"]):
            item_data["id"] = i  # Mock ID for sync interface
            item_data["bill_id"] = bill_dict["id"]
            items.append(Item(**item_data))

        bill_dict.pop("items")
        bill = Bill(**bill_dict)
        bill.items = items
        return bill

    async def get_bills_by_user(self, user_id: Any) -> List[Bill]:
        cursor = self.db.bills.find({"user_id": str(user_id)})
        bills_dicts = await cursor.to_list(length=100)

        bills = []
        for d in bills_dicts:
            d["id"] = str(d.pop("_id"))
            items_data = d.pop("items", [])
            items = [
                Item(**{**item, "id": i, "bill_id": d["id"]})
                for i, item in enumerate(items_data)
            ]
            bill = Bill(**d)
            bill.items = items
            bills.append(bill)
        return bills

    async def get_price_history(self, user_id: Any, item_name: str) -> List[Any]:
        # MongoDB Aggregation to simulate join
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
        cursor = self.db.bills.aggregate(pipeline)
        results = await cursor.to_list(length=100)

        history = []
        for r in results:
            item_data = r["items"]
            item_data["id"] = 0  # Mock
            item_data["bill_id"] = str(r["_id"])
            item = Item(**item_data)

            r["id"] = str(r.pop("_id"))
            r.pop("items")
            bill = Bill(**r)
            history.append((item, bill))
        return history
