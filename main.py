import os
from typing import Union
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv
from database.connection import engine, SessionLocal, Base
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.role import Role
# from app.models import Base
from database.seeders.seed_roles import seed_roles
from typing import Generator

from sqlalchemy.exc import SQLAlchemyError



# from database import config
from routes.base import api_router
# load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def create_tables():
	Base.metadata.create_all(bind=engine)

def include_router(app):
	app.include_router(api_router)

# app = FastAPI()
def start_application():
    app = FastAPI(title=os.getenv("PROJECT_NAME"),version=os.getenv("PROJECT_VERSION"))
    # app = FastAPI(docs_url='/api/documentation', title=os.getenv("PROJECT_NAME"),version=os.getenv("PROJECT_VERSION"))
    create_tables()
    include_router(app)
    return app

app = start_application()

# Add Role seeder
@app.on_event("startup")
def add_seed_roles():
    try:
        db = SessionLocal()
        seed_roles(db)
    except SQLAlchemyError as e:
        print(f"Error occurred during database seeding: {e}")
        # Optionally, handle the error gracefully, log it, or raise a custom exception.
    finally:
        db.close()
# End Role seeder















class Item(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    tax : Union[float, None] = None

class Item2(BaseModel):
    name : int    

@app.post("/items123", response_model=Item2, response_class=ORJSONResponse)
async def create_items123(item: Item):
    # return item
    mydata = {"name":"sss"}
    return ORJSONResponse(content=mydata,status_code=200)

@app.get("/user1/{user-id}")
def list_item(user_id: int):
    return {"message": f"Hello, list user id {user_id} route! atul"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Union[str, None] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item




