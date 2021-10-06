import os

from fastapi_login import LoginManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import pytest

from src.db.base import Base


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///test_database.sqlite")


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def secret() -> str:
    return os.urandom(24).hex()


@pytest.fixture(scope="session")
def token_url() -> str:
    return "/auth/token"


@pytest.fixture()
def clean_manager(secret, token_url) -> LoginManager:
    return LoginManager(secret, token_url)
