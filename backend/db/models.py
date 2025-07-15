from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

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
