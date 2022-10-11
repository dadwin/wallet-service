import pytest
from sqlalchemy.orm import Session
from app import models, services, schemas


def test_create_transfer_no_sender(db: Session):
    cmd = schemas.TransferCommand(amount=10,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NoSenderError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer_no_receiver(db: Session):

    db.add(models.Account(user_id="yunus", name="current"))
    db.commit()

    cmd = schemas.TransferCommand(amount=10,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NoReceiverError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer_negative_amount(db: Session):
    cmd = schemas.TransferCommand(amount=0,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NegativeAmountError):
        services.create_transfer(db, "yunus", cmd)

    cmd = schemas.TransferCommand(amount=-10,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.NegativeAmountError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer_too_big_amount(db: Session):
    cmd = schemas.TransferCommand(amount=services.AMOUNT_MAX,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.TooBigAmountError):
        services.create_transfer(db, "yunus", cmd)

    cmd = schemas.TransferCommand(amount=services.AMOUNT_MAX + 1,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.TooBigAmountError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer_no_funds(db: Session):
    cmd = schemas.TransferCommand(amount=10000,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    with pytest.raises(services.InsufficientFundsError):
        services.create_transfer(db, "yunus", cmd)


def test_create_transfer(db: Session):

    cmd = schemas.TransferCommand(amount=100,
                                  message="the first money transfer",
                                  receiver_id="andrew")

    services.create_transfer(db, "yunus", cmd)

    sender_account = services.get_account_balance("yunus")
    receiver_account = services.get_account_balance("andrew")


