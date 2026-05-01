from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # sqlite or mongodb
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pennywise")

# SQLite configuration
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# MongoDB configuration
mongo_client = AsyncIOMotorClient(MONGODB_URL)
mongo_db = mongo_client[DATABASE_NAME]


def create_db_and_tables():
    if DATABASE_TYPE == "sqlite":
        SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_mongo_db():
    return mongo_db
