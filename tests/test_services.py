import pytest
from sqlalchemy.orm import Session
from app import models, services, schemas


def test_conftest(db: Session):
    pass


def test_create_transfer_no_sender(db: Session):
    cmd = schemas.TransferCommand(amount=10,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NoSenderError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer_no_receiver(db: Session):
    db.add(models.Account(user_id="yunus", name="current", amount=0))
    db.commit()

    cmd = schemas.TransferCommand(amount=10,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NoReceiverError):
        services.create_transfer(db, "yunus", cmd)


@pytest.mark.parametrize("amount", [0, -1, -100])
def test_create_transfer_negative_amount(db: Session, amount: int):
    cmd = schemas.TransferCommand(amount=amount,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NegativeAmountError):
        services.create_transfer(db, "yunus", cmd)


@pytest.mark.parametrize("amount", [services.AMOUNT_MAX, services.AMOUNT_MAX + 1, services.AMOUNT_MAX + 100])
def test_create_transfer_too_big_amount(db: Session, amount: int):
    cmd = schemas.TransferCommand(amount=amount,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.TooBigAmountError):
        services.create_transfer(db, "yunus", cmd)


@pytest.mark.parametrize("amount", [1, 543, 25646])
def test_create_transfer_no_funds(db: Session, amount: int):
    db.add(models.Account(user_id="yunus", name="current", amount=0))
    db.add(models.Account(user_id="andrew", name="current", amount=0))
    db.commit()

    cmd = schemas.TransferCommand(amount=amount,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.InsufficientFundsError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer(db: Session):
    sender_uid = "yunus"
    receiver_uid = "andrew"
    sender_account = models.Account(user_id=sender_uid, name="current", amount=1)
    receiver_account = models.Account(user_id=receiver_uid, name="current", amount=0)
    db.add(sender_account)
    db.add(receiver_account)
    db.commit()

    cmd = schemas.TransferCommand(amount=1,
                                  message="the first money transfer",
                                  receiver_id=receiver_uid)
    services.create_transfer(db, sender_uid, cmd)
    db.refresh(sender_account)
    db.refresh(receiver_account)
    assert sender_account.amount == 0
    assert receiver_account.amount == 1
    trxs = db.query(models.Transaction).all()
    assert len(trxs) == 1
    assert trxs[0].amount == cmd.amount
    assert trxs[0].sender_id == sender_account.id
    assert trxs[0].receiver_id == receiver_account.id
    assert trxs[0].message == cmd.message


@pytest.mark.skip
def test_deadlock():
    from app.internal.database import SessionLocal, engine
    from app.models.base import Base
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()  # type: Session
    db.execute("select * from accounts;")

    with SessionLocal() as db1:
        db1.execute("drop table accounts;")
        db1.commit()
