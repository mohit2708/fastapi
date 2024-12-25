from typing import Union
from fastapi import FastAPI
import os
from dotenv import load_dotenv

from database.connection import engine, Base, SessionLocal
# for models
from database.models.roles import Role
from database.models.users import User
# for seeder
from database.seeders.roles import seed_roles
from routes.base import api_router

# from pathlib import Path

# Load .env file
load_dotenv()
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

def create_tables():
	Base.metadata.create_all(bind=engine)

def include_router(app):
	app.include_router(api_router)

# app = FastAPI(title=os.getenv("PROJECT_NAME"),version=os.getenv("PROJECT_VERSION"))
def start_application():
    app = FastAPI(title=os.getenv("PROJECT_NAME"),version=os.getenv("PROJECT_VERSION"))
    create_tables()
    include_router(app)
    return app

app = start_application()

@app.on_event("startup")
def add_seed_roles():
    db = SessionLocal()
    seed_roles(db)
    db.close()


@app.get("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}
