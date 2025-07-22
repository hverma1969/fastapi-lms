import os
from os import getenv
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = f"postgresql://{getenv('DB_USER')}:{getenv('DB_PASS')}@{getenv('DB_HOST')}:{getenv('DB_PORT')}/{getenv('DB_NAME')}"
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
