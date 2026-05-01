from sqlmodel import SQLModel, create_engine, Session
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

# ── SQLite ──────────────────────────────────────────────────────────────────
_sqlite_url = "sqlite:///database.db"
_engine = create_engine(_sqlite_url, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    """Create all SQLModel tables. Called once at startup."""
    if settings.database_type == "sqlite":
        # Ensure all models are imported before create_all
        import app.models  # noqa: F401

        SQLModel.metadata.create_all(_engine)


def get_session():
    with Session(_engine) as session:
        yield session


# ── MongoDB ──────────────────────────────────────────────────────────────────
_mongo_client = AsyncIOMotorClient(settings.mongodb_url)
_mongo_db = _mongo_client[settings.database_name]


def get_mongo_db():
    return _mongo_db
