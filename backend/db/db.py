from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.models import Base

DATABASE_URL = "sqlite:///transactions.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
