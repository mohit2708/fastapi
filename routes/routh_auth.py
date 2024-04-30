from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database.models.user import User
from datetime import datetime
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext
from database.connection import get_db
from database.schemas.user import UserCreate
from typing import List

router = APIRouter()



# Registration endpoint
@router.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter(User.user_name == user.user_name).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create user
    hashed_password = hash_password(user.password)
    db_user = User(**user.dict(), password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully"}

# Login endpoint
@router.post("/login/")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Here you might want to generate a JWT token for authentication
    return {"message": "Login successful"}

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register1/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user with the provided username or email already exists
    existing_user_username = get_user_by_username(db, user.user_name)
    existing_user_email = get_user_by_email(db, user.email)

    if existing_user_username or existing_user_email:
        message = "User name already registered" if existing_user_username else "Email already registered"
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": message,
            },
            status_code=400
        )
    
    # Hash the password before storing it
    hash_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Create a new user with the hashed password
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        user_name=user.user_name,
        email=user.email,
        password=hash_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
