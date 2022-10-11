from app import schemas
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
    pass


def get_transfers(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    pass


def get_account_balance(user_id: str):
    pass
