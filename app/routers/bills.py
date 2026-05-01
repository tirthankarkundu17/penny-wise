from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.dependencies import get_current_user
from app.db.repositories import get_repository
from app.db.repositories.base import BaseRepository
from app.models.user import User
from app.schemas.bill import BillRead
from app.services.gemini_service import GeminiService

router = APIRouter(prefix="/bills", tags=["Bills"])

_gemini = GeminiService()


@router.post("/upload", response_model=BillRead)
async def upload_receipt(
    file: UploadFile = File(...),
    repo: BaseRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> BillRead:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    try:
        extracted_data = _gemini.extract_receipt_data(image_bytes)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gemini extraction failed: {exc}")

    return await repo.create_bill(current_user.id, extracted_data)


@router.get("/", response_model=List[BillRead])
async def list_bills(
    repo: BaseRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user),
) -> List[BillRead]:
    return await repo.get_bills_by_user(current_user.id)
