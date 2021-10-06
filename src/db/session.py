from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from src.db.settings import models_to_import, uri_db, create_tables  # NoQA
from .base import Base


@contextmanager
def db_session(db_url: str = uri_db, create_tables: bool = create_tables):
    engine = get_engine(db_url)
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    if create_tables:
        Base.metadata.create_all(engine)
    yield db_session
    db_session.close()
    connection.close()


def get_engine(db_url: str = uri_db) -> Engine:
    return create_engine(db_url, convert_unicode=True, pool_size=20, poolclass=QueuePool)
