from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from users.models import Base
import pytest


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