import pytest
from sqlalchemy.orm import Session
from app import models, services, schemas


def test_get_transfers_no_user(db: Session):
    with pytest.raises(services.NoUserAccountError):
        services.get_transfers(db, "yunus")


def test_get_transfers_no_transfers(db: Session):
    account = models.Account(user_id="yunus", name="current", amount=1)
    db.add(account)
    db.commit()

    transfers = services.get_transfers(db, "yunus")
    assert len(transfers) == 0


@pytest.mark.parametrize("number", [1, 4, 46])
def test_get_transfers(db: Session, number: int):
    account1 = models.Account(id=1, user_id="yunus", name="current", amount=0)
    account2 = models.Account(id=2, user_id="nick", name="current", amount=0)
    db.add(account1)
    db.add(account2)

    for i in range(number):
        db.add(models.Transaction(amount=i + 1,
                                  message=f"transfer #{i}",
                                  sender_id=account1.id,
                                  receiver_id=account2.id))
    db.commit()

    transfers = services.get_transfers(db, "yunus")
    assert len(transfers) == number

    transfers = services.get_transfers(db, "nick")
    assert len(transfers) == number


def test_transfers_two_users(db: Session):
    sender_uid = "yunus"
    receiver_uid = "andrew"
    sender_account = models.Account(user_id=sender_uid, name="current", amount=1)
    receiver_account = models.Account(user_id=receiver_uid, name="current", amount=0)
    db.add(sender_account)
    db.add(receiver_account)
    db.commit()

    cmd1 = schemas.TransferCommand(amount=1,
                                   message="the first money transfer",
                                   receiver_id=receiver_uid)
    services.create_transfer(db, sender_uid, cmd1)
    cmd2 = schemas.TransferCommand(amount=1,
                                   message="the second money transfer",
                                   receiver_id=sender_uid)
    services.create_transfer(db, receiver_uid, cmd2)

    transfers = services.get_transfers(db, "yunus")
    assert len(transfers) == 2
    assert transfers[0].amount == 1
    assert transfers[0].message == "the first money transfer"
    assert transfers[0].sender_id == sender_uid
    assert transfers[0].receiver_id == receiver_uid

    assert transfers[1].amount == 1
    assert transfers[1].message == "the second money transfer"
    assert transfers[1].sender_id == receiver_uid
    assert transfers[1].receiver_id == sender_uid


def test_transfer_three_users(db: Session):
    pass


def test_transfer_offset_limit(db: Session):
    pass
