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


AMOUNT_MAX = 1000000


def create_transfer(db: Session, user_id: str, cmd: schemas.TransferCommand):
    with db:
        sender_account = db.query(models.Account).filter(models.Account.user_id == user_id).first()
        if not sender_account:
            raise NoSenderError(f"no account for sender {user_id}")

        receiver_account = db.query(models.Account).filter(models.Account.user_id == cmd.receiver_id).first()
        if not receiver_account:
            raise NoReceiverError(f"no account for receiver {cmd.receiver_id}")


def get_transfers(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    pass


def get_account_balance(user_id: str):
    pass
