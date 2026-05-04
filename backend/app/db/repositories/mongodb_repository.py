import uuid
from datetime import datetime
from typing import Any, List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.repositories.base import BaseRepository
from app.models.bill import Bill
from app.models.item import Item
from app.models.user import User
from app.schemas.bill import BillCreate
from app.schemas.user import RefreshToken, UserCreate
from bson import ObjectId


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
        items_data = []
        for item in extracted_data.items:
            idat = item.model_dump()
            idat["id"] = idat.get("hsn") or str(uuid.uuid4())
            items_data.append(idat)

        doc = {
            "user_id": str(user_id),
            "store_name": extracted_data.store_name,
            "bill_date": extracted_data.bill_date,
            "bill_number": extracted_data.bill_number,
            "grand_total": extracted_data.grand_total,
            "created_at": datetime.utcnow(),
            "items": items_data,
        }
        result = await self.db.bills.insert_one(doc)
        bill_id = str(result.inserted_id)
        doc["id"] = bill_id

        items = [Item(**{**idat, "bill_id": bill_id}) for idat in items_data]
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
            items = [Item(**{**item, "bill_id": doc["id"]}) for item in items_data]
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
            item_data.update({"bill_id": str(r["_id"])})
            item = Item(**item_data)
            r["id"] = str(r.pop("_id"))
            r.pop("items")
            bill = Bill(**r)
            history.append((item, bill))
        return history

    async def delete_bill(self, user_id: Any, bill_id: Any) -> bool:
        try:
            result = await self.db.bills.delete_one(
                {"_id": ObjectId(bill_id), "user_id": str(user_id)}
            )
            return result.deleted_count > 0
        except Exception:
            return False

    async def delete_item(self, user_id: Any, item_id: Any) -> bool:
        # We search for the bill belonging to the user and containing an item with matching ID or HSN
        result = await self.db.bills.update_one(
            {"user_id": str(user_id)},
            {"$pull": {"items": {"$or": [{"id": item_id}, {"hsn": item_id}]}}},
        )
        return result.modified_count > 0

    async def get_refresh_token_by_value(self, refresh_token: str) -> str | None:
        doc = await self.db.users.find_one({"refresh_token": refresh_token})
        if doc:
            return doc["refresh_token"]
        return None

    async def update_refresh_token(self, user_id: Any, new_refresh_token: str):
        print(f"Updating refresh token for user_id={user_id} to new_refresh_token={new_refresh_token}")
        await self.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"refresh_token": new_refresh_token}})
        return await self.get_refresh_token_by_value(new_refresh_token)  # Refresh the object from the database
