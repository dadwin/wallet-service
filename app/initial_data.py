import logging

from app import models
from app.internal.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    db.query(models.Account).delete()
    db.query(models.Transaction).delete()
    db.add(models.Account(user_id="house", name="current", amount=1000000))
    db.add(models.Account(user_id="yunus", name="current", amount=0))
    db.add(models.Account(user_id="andrew", name="current", amount=0))
    db.add(models.Account(user_id="nick", name="current", amount=0))
    db.commit()


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
