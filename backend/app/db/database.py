from sqlmodel import SQLModel, create_engine, Session
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

# ── SQLite ──────────────────────────────────────────────────────────────────
_sqlite_url = "sqlite:///database.db"
_engine = create_engine(_sqlite_url, connect_args={"check_same_thread": False})


async def create_db_and_tables() -> None:
    """Create all SQLModel tables or MongoDB indices. Called once at startup."""
    if settings.database_type == "sqlite":
        # Ensure all models are imported before create_all
        import app.models  # noqa: F401

        SQLModel.metadata.create_all(_engine)
    elif settings.database_type == "mongodb":
        # Create unique index for bills (store_name + bill_number)
        await _mongo_db.bills.create_index(
            [("bill_number", 1), ("store_name", 1)],
            unique=True,
            partialFilterExpression={
                "bill_number": {"$type": "string"}
            },  # Don't conflict on nulls
        )


def get_session():
    with Session(_engine) as session:
        yield session


# ── MongoDB ──────────────────────────────────────────────────────────────────
_mongo_client = AsyncIOMotorClient(settings.mongodb_url)
_mongo_db = _mongo_client[settings.database_name]


def get_mongo_db():
    return _mongo_db
