import uvicorn
import logging
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pymongo.errors import DuplicateKeyError

from app.core.config import settings
from app.db.database import create_db_and_tables
from app.routers import auth_router, bills_router, analytics_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(
    title=settings.app_name,
    description="AI-powered grocery receipt tracker with JWT auth and swappable database backends.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Exception Handlers ────────────────────────────────────────────────────────
@app.exception_handler(IntegrityError)
async def sqlalchemy_integrity_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Database conflict: A record with these details already exists."
        },
    )


@app.exception_handler(DuplicateKeyError)
async def mongodb_duplicate_key_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Duplicate entry: This bill has already been uploaded for this store."
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    # Log the full error here in a real app
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(bills_router)
app.include_router(analytics_router)


# ── Lifecycle ─────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup() -> None:
    await create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
