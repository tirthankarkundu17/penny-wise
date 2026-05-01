from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uvicorn

from fastapi.security import OAuth2PasswordRequestForm
from app.database import create_db_and_tables, get_session
from app.models import Bill, Item, User
from app.schemas import BillRead, PriceHistory, UserCreate, UserRead, Token
from app.services.gemini_service import GeminiService
from app.auth import (
    get_current_user,
    get_password_hash,
    verify_password,
    create_access_token,
)

app = FastAPI(title="Penny Wise - Grocery Tracker")
gemini_service = GeminiService()


@app.post("/register", response_model=UserRead)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/upload", response_model=BillRead)
async def upload_receipt(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
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

    # Save to database
    db_bill = Bill(
        user_id=current_user.id,
        store_name=extracted_data.store_name,
        bill_date=extracted_data.bill_date,
        bill_number=extracted_data.bill_number,
        grand_total=extracted_data.grand_total,
    )
    session.add(db_bill)
    session.commit()
    session.refresh(db_bill)

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
        session.add(db_item)

    session.commit()
    session.refresh(db_bill)
    return db_bill


@app.get("/bills", response_model=List[BillRead])
def list_bills(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    bills = session.exec(select(Bill).where(Bill.user_id == current_user.id)).all()
    return bills


@app.get("/price-history/{item_name}", response_model=List[PriceHistory])
def get_price_history(
    item_name: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    # Simple search by item name (case-insensitive) for current user
    statement = (
        select(Item, Bill)
        .join(Bill)
        .where(Bill.user_id == current_user.id)
        .where(Item.item_name.ilike(f"%{item_name}%"))
        .order_by(Bill.bill_date)
    )
    results = session.exec(statement).all()

    history = []
    for item, bill in results:
        history.append(
            PriceHistory(
                date=bill.bill_date, price=item.net_price, store=bill.store_name
            )
        )

    return history


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
