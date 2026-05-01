from fastapi import Depends
from sqlmodel import Session

from app.core.config import settings
from app.db.database import get_session, get_mongo_db
from app.db.repositories.base import BaseRepository
from app.db.repositories.sql_repository import SQLRepository
from app.db.repositories.mongodb_repository import MongoDBRepository


def get_repository(
    session: Session = Depends(get_session),
    mongo_db=Depends(get_mongo_db),
) -> BaseRepository:
    if settings.database_type == "sqlite":
        return SQLRepository(session)
    elif settings.database_type == "mongodb":
        return MongoDBRepository(mongo_db)
    raise ValueError(f"Unsupported DATABASE_TYPE: {settings.database_type}")
