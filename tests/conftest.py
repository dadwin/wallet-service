from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.internal.database import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
