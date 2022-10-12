import pytest
from sqlalchemy.orm import Session
from app import models, services, schemas


def test_get_balance_no_user(db: Session):
    with pytest.raises(services.NoUserAccountError):
        services.get_account_balance_by_user(db, "yunus")


def test_get_balance(db: Session):
    account = models.Account(user_id="yunus", name="current", amount=1)
    db.add(account)
    db.commit()

    user_account = services.get_account_balance_by_user(db, "yunus")
    assert account.user_id == user_account.user_id
    assert account.name == user_account.name
    assert account.amount == user_account.amount
    assert account.id == user_account.account_id
