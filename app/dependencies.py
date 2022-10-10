from fastapi import HTTPException

from app.internal.database import SessionLocal


async def get_query_token(token: str):
    if token != "thunes":
        raise HTTPException(status_code=401, detail="No token provided")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
