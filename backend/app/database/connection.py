from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# Add DATABASE_URL to settings or construct it here
# Example: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/kis_invest")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
