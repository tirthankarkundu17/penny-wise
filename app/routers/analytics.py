from typing import List

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.db.repositories import get_repository
from app.db.repositories.base import BaseRepository
from app.models.user import User
from app.schemas.bill import PriceHistory

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/price-history/{item_name}", response_model=List[PriceHistory])
async def get_price_history(
    item_name: str,
    repo: BaseRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> List[PriceHistory]:
    results = await repo.get_price_history(current_user.id, item_name)
    return [
        PriceHistory(
            date=bill.bill_date,
            price=item.net_price,
            store=bill.store_name,
            bill_date=bill.bill_date,
            bill_number=bill.bill_number,
            item_name=item.item_name,
            item_description=item.description,
        )
        for item, bill in results
    ]
