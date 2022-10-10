from pydantic import BaseModel
from datetime import datetime


class AccountBalance(BaseModel):
    account_id: int
    name: str
    user_id: int
    amount: int


class TransferInfo(BaseModel):
    sender_id: int
    receiver_id: int
    amount: int
    message: str
    created_at: datetime


class TransferCommand(BaseModel):
    amount: int
    message: str
    receiver_id: int
