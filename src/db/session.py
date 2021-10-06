from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from src.db.settings import models_to_import, uri_db, create_tables  # NoQA
from .base import Base

engine = create_engine(uri_db, convert_unicode=True, pool_size=20, poolclass=QueuePool)


@contextmanager
def db_session(create_tables: bool = create_tables):
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    if create_tables:
        Base.metadata.create_all(engine)
    yield db_session
    db_session.close()
    connection.close()
