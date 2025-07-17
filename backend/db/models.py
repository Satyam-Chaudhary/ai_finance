from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(String, primary_key=True)
    bank = Column(String)
    amount = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime)
    account_number = Column(String)
    category = Column(String)
    suspicious_reason = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="transactions")



