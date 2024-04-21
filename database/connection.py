import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


MY_SQL_USER     = os.getenv("MY_SQL_USER")
MY_SQL_SERVER   = os.getenv("MY_SQL_SERVER")
MY_SQL_PASSWORD = os.getenv("MY_SQL_PASSWORD")
MY_SQL_PORT     = os.getenv("MY_SQL_PORT")
MY_SQL_DATABASE = os.getenv("MY_SQL_DATABASE")

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/profile_fastapi"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{MY_SQL_USER}:@{MY_SQL_SERVER}/{MY_SQL_DATABASE}"

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

