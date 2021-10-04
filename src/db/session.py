from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .base import Base
from src.db.settings import models_to_import, uri_db  # NoQA


def create_engine_to_connect(uri_db: str):
    return create_engine(uri_db)


def create_tables_if_not_exist(uri_db):
    Base.metadata.create_all(create_engine_to_connect(uri_db))


def get_db(uri_db: str = uri_db, create_tables: bool = True) -> Session:
    engine = create_engine_to_connect(uri_db)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    if create_tables:
        create_tables_if_not_exist(uri_db)
    try:
        yield session
    finally:
        session.close()
