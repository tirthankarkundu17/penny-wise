from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from typing import List
import uvicorn
from app.database import create_db_and_tables
from app.models import Bill, Item, User
from app.schemas import BillRead, PriceHistory, UserCreate, UserRead, Token, UserLogin
from app.services.gemini_service import GeminiService
from app.repositories import get_repository
from app.repositories.base import BaseRepository
from app.auth import (
    get_current_user,
    get_password_hash,
    verify_password,
    create_access_token,
)

app = FastAPI(title="Penny Wise - Grocery Tracker")
gemini_service = GeminiService()


@app.post("/register", response_model=UserRead)
def register_user(user: UserCreate, repo: BaseRepository = Depends(get_repository)):
    # Check if user already exists
    existing_user = repo.get_user_by_username(user.username) or repo.get_user_by_email(
        user.email
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    hashed_password = get_password_hash(user.password)
    return repo.create_user(user, hashed_password)


@app.post("/login", response_model=Token)
def login_for_access_token(
    login_data: UserLogin,
    repo: BaseRepository = Depends(get_repository),
):
    user = repo.get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES

    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/upload", response_model=BillRead)
async def upload_receipt(
    file: UploadFile = File(...),
    repo: BaseRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    image_bytes = await file.read()

    try:
        extracted_data = gemini_service.extract_receipt_data(image_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Gemini extraction failed: {str(e)}"
        )

    return repo.create_bill(current_user.id, extracted_data)


@app.get("/bills", response_model=List[BillRead])
def list_bills(
    repo: BaseRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user),
):
    return repo.get_bills_by_user(current_user.id)


@app.get("/price-history/{item_name}", response_model=List[PriceHistory])
def get_price_history(
    item_name: str,
    repo: BaseRepository = Depends(get_repository),
    current_user: User = Depends(get_current_user),
):
    results = repo.get_price_history(current_user.id, item_name)

    history = []
    for item, bill in results:
        history.append(
            PriceHistory(
                date=bill.bill_date,
                price=item.net_price,
                store=bill.store_name,
                bill_date=bill.bill_date,
                bill_number=bill.bill_number,
                item_name=item.item_name,
                item_description=item.description,
            )
        )

    return history


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
