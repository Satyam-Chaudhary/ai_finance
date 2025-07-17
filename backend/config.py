import os
from dotenv import load_dotenv

load_dotenv()


SUSPICIOUS_TOPIC = "suspicious-transactions"


SECRET_KEY = os.getenv("SECRET_KEY", "satyam-is-depressed")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance.db")
