from sqlalchemy import Boolean, Column, ForeignKey, Integer, DECIMAL, String
from sqlalchemy.orm import relationship

from app.models.base_class import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(String, index=True)
    amount = Column(Integer)
    # currency_alpha_code = Column(String)
    # currency_num_code = Column(Integer)

# about amount/money https://stackoverflow.com/questions/15726535/which-datatype-should-be-used-for-currency
# https://www.iso.org/iso-4217-currency-codes.html
