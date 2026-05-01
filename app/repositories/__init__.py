from fastapi import Depends
from sqlmodel import Session
from app.database import get_session, DATABASE_TYPE, get_mongo_db
from app.repositories.sql_repository import SQLRepository
from app.repositories.mongodb_repository import MongoDBRepository
from app.repositories.base import BaseRepository


def get_repository(
    session: Session = Depends(get_session), mongo_db=Depends(get_mongo_db)
) -> BaseRepository:
    if DATABASE_TYPE == "sqlite":
        return SQLRepository(session)
    elif DATABASE_TYPE == "mongodb":
        return MongoDBRepository(mongo_db)
    else:
        raise ValueError(f"Unsupported DATABASE_TYPE: {DATABASE_TYPE}")
