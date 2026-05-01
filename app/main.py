import uvicorn
from fastapi import FastAPI, status

from app.core.config import settings
from app.db.database import create_db_and_tables
from app.routers import auth_router, bills_router, analytics_router

from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pymongo.errors import DuplicateKeyError

app = FastAPI(
    title=settings.app_name,
    description="AI-powered grocery receipt tracker with JWT auth and swappable database backends.",
    version="1.0.0",
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
