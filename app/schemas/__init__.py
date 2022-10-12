from pydantic import BaseModel
from datetime import datetime


class AccountBalance(BaseModel):
    account_id: int
    name: str
    user_id: str
    amount: int
    created_at: datetime
    updated_at: datetime


class TransferInfo(BaseModel):
    sender_id: str
    receiver_id: str
    amount: int
    message: str
    created_at: datetime


class TransferCommand(BaseModel):
    amount: int
    # currency_code: str
    message: str
    receiver_id: str
