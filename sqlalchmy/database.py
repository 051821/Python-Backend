# 1
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from .config import settings

# 👇 FORCE correct path
# BASE_DIR = Path(__file__).resolve().parent
# env_path = BASE_DIR / ".env"

# load_dotenv(dotenv_path=env_path)

# DATABASE_URL = os.getenv("DATABASE_URL")

# print("DATABASE_URL =", DATABASE_URL)

DATABASE_URL = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}'

# PostgreSQL connection URL
# Format: postgresql://username:password@host:port/database_name

# Create engine (connects to database)
engine = create_engine(DATABASE_URL,echo = True)

# SessionLocal = session factory (used to interact with DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("Connected to DB:", engine.url)