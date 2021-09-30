from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base
from src.db.settings import models_to_import, uri_db  # NoQA

engine = create_engine(uri_db)
Base.metadata.create_all(engine)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
