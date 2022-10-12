from typing import List

from app import schemas, models
from sqlalchemy.orm import Session


class ErrorBase(Exception):
    """Base error"""


class NoReceiverError(ErrorBase):
    """Receiver does not exists"""


class NoSenderError(ErrorBase):
    """Sender does not exists"""


class NegativeAmountError(ErrorBase):
    """Transferred amount is negative"""


class TooBigAmountError(ErrorBase):
    """Transferred amount is too big"""


class InsufficientFundsError(ErrorBase):
    """Sender has insufficient funds"""


class NoUserAccountError(ErrorBase):
    """"""


AMOUNT_MAX = 1000000


def create_transfer(db: Session, user_id: str, cmd: schemas.TransferCommand) -> schemas.TransferInfo:
    if cmd.amount <= 0:
        raise NegativeAmountError

    if cmd.amount >= AMOUNT_MAX:
        raise TooBigAmountError

    sender_account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not sender_account:
        raise NoSenderError(f"no account for sender {user_id}")

    receiver_account = db.query(models.Account).filter(models.Account.user_id == cmd.receiver_id).first()
    if not receiver_account:
        raise NoReceiverError(f"no account for receiver {cmd.receiver_id}")
    print(sender_account.amount)
    if sender_account.amount < cmd.amount:
        raise InsufficientFundsError

    sender_account.amount -= cmd.amount
    receiver_account.amount += cmd.amount
    db.add(sender_account)
    db.add(receiver_account)
    trx = models.Transaction(amount=cmd.amount,
                             message=cmd.message,
                             sender_id=sender_account.id,
                             receiver_id=receiver_account.id)
    db.add(trx)
    db.commit()
    db.refresh(trx)
    return schemas.TransferInfo(sender_id=user_id,
                                receiver_id=cmd.receiver_id,
                                amount=cmd.amount,
                                message=cmd.message,
                                created_at=trx.created_at)


def get_transfers(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[schemas.TransferInfo]:
    user_account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
    if not user_account:
        raise NoUserAccountError

    transactions = db. \
        query(models.Transaction). \
        filter((models.Transaction.sender_id == user_account.id) | (models.Transaction.receiver_id == user_account.id)). \
        order_by(models.Transaction.created_at.desc()). \
        offset(skip). \
        limit(limit). \
        all()

    return [schemas.TransferInfo(sender_id=trx.sender_account.user_id,
                                 receiver_id=trx.receiver_account.user_id,
                                 amount=trx.amount,
                                 message=trx.message,
                                 created_at=trx.created_at,
                                 ) for trx in transactions]


def get_account_balance(db: Session, account_id: int):
    balance = 0
    for trx in db.query(models.Transaction).filter(models.Transaction.account_id == account_id).all():
        balance += trx.amount
    return balance


def get_account_balance_by_user(db: Session, user_id: str):
    pass
