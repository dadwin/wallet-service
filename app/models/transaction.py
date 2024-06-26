from sqlalchemy import Boolean, Column, ForeignKey, Integer, DECIMAL, String, DateTime
from sqlalchemy.orm import relationship
from app.models.mixins import CreatedAtMixin

from app.models.base_class import Base


class Transaction(Base, CreatedAtMixin):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    message = Column(String)
    sender_id = Column(Integer, ForeignKey("accounts.id"), index=True)
    receiver_id = Column(Integer, ForeignKey("accounts.id"), index=True)

    sender_account = relationship("Account", foreign_keys=[sender_id])
    receiver_account = relationship("Account", foreign_keys=[receiver_id])
