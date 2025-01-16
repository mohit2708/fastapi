from database.connection import engine, Base, SessionLocal
from database.seeders.roles import seed_roles
from database.connection import engine, Base
from database.models.roles import Role
from routes.base import api_router
from dotenv import load_dotenv
from fastapi import FastAPI
from typing import Union

import os


# Load .env file
load_dotenv()

# add code for routes
def include_router(app):
	app.include_router(api_router)

def create_tables():
	Base.metadata.create_all(bind=engine)

def start_application():
    # app = FastAPI(title=project_config.PROJECT_NAME,version=project_config.PROJECT_VERSION)
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
