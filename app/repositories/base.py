from abc import ABC, abstractmethod
from typing import List, Optional, Any
from app.models import User, Bill, Item
from app.schemas import UserCreate, BillCreate


class BaseRepository(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_bill(self, user_id: Any, bill_data: Any) -> Bill:
        pass

    @abstractmethod
    def get_bills_by_user(self, user_id: Any) -> List[Bill]:
        pass

    @abstractmethod
    def get_price_history(self, user_id: Any, item_name: str) -> List[Any]:
        pass
