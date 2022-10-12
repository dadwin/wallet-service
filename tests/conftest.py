from typing import Dict, Generator

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.base import Base
from app.internal.database import SessionLocal, engine
from app.main import app

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db1() -> Generator:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sqlalchemy.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session
    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()
