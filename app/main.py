import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.db.database import create_db_and_tables
from app.routers import auth_router, bills_router, analytics_router

app = FastAPI(
    title=settings.app_name,
    description="AI-powered grocery receipt tracker with JWT auth and swappable database backends.",
    version="1.0.0",
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
