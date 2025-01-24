from database.connection import engine, Base, SessionLocal
from database.seeders.roles import seed_roles
from database.connection import engine, Base
from jwt.exceptions import InvalidTokenError
from fastapi.responses import JSONResponse
from database.models.roles import Role
from routes.base import api_router
from dotenv import load_dotenv
from fastapi import FastAPI,Request, HTTPException
from typing import Union
import jwt
from core.config import jwt_config


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

# Define the middleware function
async def role_check_middleware(request: Request, call_next):
    # Exclude the login route from the role check
    if request.url.path == "/login":
        response = await call_next(request)
        return response

    token = request.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    try:
        payload = jwt.decode(token[7:], jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        print(payload)
        email: str = payload.get("email")
        role_id: int = payload.get("role_id")
        if email is None or role_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if role_id != 1:
            return JSONResponse(status_code=403, content={"message": "You are not authorized to access this resource"})
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    response = await call_next(request)
    return response

# app.middleware("http")(role_check_middleware)