from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from typing import List
import uvicorn

from app.database import create_db_and_tables, get_session
from app.models import Bill, Item
from app.schemas import BillRead, PriceHistory
from app.services.gemini_service import GeminiService

app = FastAPI(title="Penny Wise - Grocery Tracker")
gemini_service = GeminiService()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    from fastapi.responses import FileResponse
    return FileResponse('static/index.html')

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/upload", response_model=BillRead)
async def upload_receipt(file: UploadFile = File(...), session: Session = Depends(get_session)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    image_bytes = await file.read()
    
    try:
        extracted_data = gemini_service.extract_receipt_data(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini extraction failed: {str(e)}")
    
    # Save to database
    db_bill = Bill(
        store_name=extracted_data.store_name,
        bill_date=extracted_data.bill_date,
        bill_number=extracted_data.bill_number,
        grand_total=extracted_data.grand_total
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
            value=item_data.value
        )
        session.add(db_item)
    
    session.commit()
    session.refresh(db_bill)
    return db_bill

@app.get("/bills", response_model=List[BillRead])
def list_bills(session: Session = Depends(get_session)):
    bills = session.exec(select(Bill)).all()
    return bills

@app.get("/price-history/{item_name}", response_model=List[PriceHistory])
def get_price_history(item_name: str, session: Session = Depends(get_session)):
    # Simple search by item name (case-insensitive)
    statement = select(Item, Bill).join(Bill).where(Item.item_name.ilike(f"%{item_name}%")).order_by(Bill.bill_date)
    results = session.exec(statement).all()
    
    history = []
    for item, bill in results:
        history.append(PriceHistory(
            date=bill.bill_date,
            price=item.net_price,
            store=bill.store_name
        ))
    
    return history

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
