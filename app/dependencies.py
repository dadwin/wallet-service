from fastapi import Header

from app.internal.database import SessionLocal

users = {
    "thunes": "yunus"
}


async def get_user_by_token(token: str = Header()):
    user = users.get(token)  # TODO should be redis as session store
    return user


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
