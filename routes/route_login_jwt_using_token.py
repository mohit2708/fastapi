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



# from jose import jwt, JWTError


router = APIRouter()

@router.post("/login")
async def login(email:str, password:str, db:Session = Depends(get_db)):
    get_user_data = User.get_user_by_email(db, email)
    if not get_user_data:
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "Email ID does not exist",
            },
            status_code=404
        )
    if not User.verify_password(password, get_user_data.password):
        # raise HTTPException(status_code=401, detail="Incorrect password")
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "Password is incorrect",
            },
            status_code=404
        )

    # Here you can generate and return a JWT token for authentication if needed
    access_token_expires = timedelta(minutes=int(jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = create_access_token(
        data={"email": get_user_data.email}, expires_delta=access_token_expires
    )

    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "User login successfully!",
            "token":{
                "access_token": access_token,
                "token_type": "bearer",
            },
            "user_data": {
                "id": get_user_data.id,
                "first_name": get_user_data.first_name,
                "last_name": get_user_data.last_name,
                "created_at": get_user_data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": get_user_data.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        },
        status_code=200
    )
    # print(get_user_data)



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_config.SECRET_KEY, algorithm=jwt_config.ALGORITHM)
    return encoded_jwt



header_scheme = APIKeyHeader(name="jwt_config.API_KEY_HEADER_NAME")

def verify_token(token: str = Depends(header_scheme)):
    try:
        payload = jwt.decode(token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/users/")
async def get_users(email: str = Depends(verify_token), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users




# HTTP basic =========================================================
# from typing import Annotated

# from fastapi import Depends, FastAPI
# from fastapi.security import HTTPBasic, HTTPBasicCredentials

# app = FastAPI()

# security = HTTPBasic()


# @router.get("/users/me")
# def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
#     return {"username": credentials.username, "password": credentials.password}



# header_scheme = APIKeyHeader(name="Authorization")

# def verify_token(authorization: str = Depends(header_scheme)):
#     try:
#         # Assuming the format is "email:password"
#         email_password = authorization.split(" ")[1]
#         email, password = email_password.split(":")
        
#         # Verify the email and password
#         if not verify_email_and_password(email, password):
#             raise HTTPException(status_code=401, detail="Invalid email or password")
        
#         return email
#     except (JWTError, ValueError):
#         raise HTTPException(status_code=401, detail="Invalid token")

# def verify_email_and_password(email: str, password: str) -> bool:
#     # Implement your email and password verification logic here
#     return True

# @router.get("/users/")
# async def get_users(email: str = Depends(verify_token), db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, jwt_config.SECRET_KEY, algorithms=[jwt_config.ALGORITHM])
#         email: str = payload.get("email")
#         if email is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return email
#     except jwt.JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# @router.get("/users/")
# async def get_users(email: str = Depends(verify_token), db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users
