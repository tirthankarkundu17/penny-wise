from abc import ABC, abstractmethod
from typing import Any, List, Optional

from app.models.user import User
from app.models.bill import Bill
from app.schemas.user import UserCreate
from app.schemas.bill import BillCreate


class BaseRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserCreate, hashed_password: str) -> User: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def create_bill(self, user_id: Any, extracted_data: BillCreate) -> Bill: ...

    @abstractmethod
    async def get_bills_by_user(self, user_id: Any) -> List[Bill]: ...

    @abstractmethod
    async def get_price_history(self, user_id: Any, item_name: str) -> List[Any]: ...
