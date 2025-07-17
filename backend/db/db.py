from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.db.models import Base

DATABASE_URL = "sqlite:///transactions.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
