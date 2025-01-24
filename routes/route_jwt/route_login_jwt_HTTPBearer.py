from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyHeader
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from database.connection import get_db
from sqlalchemy.orm import Session
from database.models.users import User
from core.config import jwt_config
from fastapi.security import HTTPBearer
from database.schemas.user import UserCreate, UserLogin

router = APIRouter()

# Define the HTTPBearer scheme
http_bearer_scheme = HTTPBearer()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
# async def login(request: UserLogin, db: Session = Depends(get_db)):
    get_user_data = User.get_user_by_email(db, form_data.username)  # Changed to get_user_by_email
    if not get_user_data:
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "Email does not exist",
            },
            status_code=404
        )
    if not User.verify_password(form_data.password, get_user_data.password):
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "Password is incorrect",
            },
            status_code=404
        )

    access_token_expires = timedelta(minutes=int(jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = create_access_token(
        data={"email": get_user_data.email}, expires_delta=access_token_expires  # Changed to include email
    )

    print(f"Generated Token: {access_token}")

    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "User login successfully!",
            "token": {
                "access_token": access_token,
                "token_type": "bearer",
            },
            "user_data": {
                "id": get_user_data.id,
                "first_name": get_user_data.first_name,
                "last_name": get_user_data.last_name,
                "created_at": get_user_data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": get_user_data.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
            "access_token": access_token,
        },
        status_code=200
    )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_config.SECRET_KEY, algorithm=jwt_config.ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(http_bearer_scheme)):
    try:
        payload = jwt.decode(token.credentials, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        email: str = payload.get("email")  # Changed to email
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        print(f"Decoded Token Payload: {payload}")
        return email
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/users/")
async def get_users(email: str = Depends(verify_token), db: Session = Depends(get_db)):  # Changed to email
    users = db.query(User).all()
    return users