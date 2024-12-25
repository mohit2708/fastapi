from fastapi import FastAPI, APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models.users import User
from database.models.roles import Role
from database.models.user_details import UserDetails

from fastapi.responses import JSONResponse  # Include for message response.
from sqlalchemy.exc import SQLAlchemyError

from database.schemas.user import UserCreate, UserLogin

import bcrypt # for hashed password 

import jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Define a SECRET_KEY and JWT expiration time
SECRET_KEY = "4564231534356412231321231354132132"  # Make sure to store this securely
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiry time

router = APIRouter()


# Define a password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password function
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password function
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


'''
Create user
role id exist or not
username or email already exist
password hash
'''
@router.post("/registration")
def registration_user(request: UserCreate, db: Session = Depends(get_db)):

    # Check if the provided role_id exists
    role = db.query(Role).filter(Role.id == request.role_id).first()
    if not role:
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "Role ID does not exist",
            },
            status_code=404
        )
    
    # Check user or email already exists or not
    existing_user_email = db.query(User).filter(User.email == request.email).first()
    existing_user_username = db.query(User).filter(User.user_name == request.user_name).first()

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
    # hash_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    hashed_password = hash_password(request.password)

    db_user = User(
            role_id=request.role_id,
            first_name=request.first_name,
            last_name=request.last_name,
            user_name=request.user_name,
            email=request.email,
            # password=request.password
            password=hashed_password  # Store the hashed password as string
        )

    # db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create and save the user details
    db_user_details = UserDetails(
        user_id=db_user.id,
        address=request.address,
        state=request.state,
        city=request.city,
        zip_code=request.zip_code
    )
    db.add(db_user_details)
    db.commit()

    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "User has been created successfully!",
            "data": {
                "id": db_user.id,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "user_name": db_user.user_name,
                "email": db_user.email,
                "address": db_user_details.address,
                "state": db_user_details.state,
                "city": db_user_details.city,
                "zip_code": db_user_details.zip_code,
                "created_at": db_user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                "updated_at": db_user.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
            }
        },
        status_code=200
    )


'''
login user
email or password is valid or not
password hash check
'''
@router.post("/login1")
def login_user1(request: UserLogin, db: Session = Depends(get_db)):

    # Check if the user exists with the provided email
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "User not found",
            },
            status_code=404
        )
    
    # Verify the provided password with the stored hashed password using pwd_context
    if not pwd_context.verify(request.password, db_user.password):
        return JSONResponse(
            content={
                "status": False,
                "code": 401,
                "message": "Invalid password",
            },
            status_code=401
        )

    # Retrieve the UserDetails associated with this user
    db_user_details = db.query(UserDetails).filter(UserDetails.user_id == db_user.id).first()

    # If login is successful
    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "Login successful",
            "data": {
                "id": db_user.id,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "user_name": db_user.user_name,
                "email": db_user.email,
                "user_details": {
                    "address": db_user_details.address if db_user_details else None,
                    "state": db_user_details.state if db_user_details else None,
                    "city": db_user_details.city if db_user_details else None,
                    "zip_code": db_user_details.zip_code if db_user_details else None,
                },
                "created_at": db_user.created_at.strftime("%Y-%m-%dT%H:%M:%S") if db_user_details else None,
                "updated_at": db_user.updated_at.strftime("%Y-%m-%dT%H:%M:%S") if db_user_details else None,
            }
        },
        status_code=200
    )



# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Update the login endpoint to return a JWT token upon successful login
@router.post("/login")
def login_user(request: UserLogin, db: Session = Depends(get_db)):
    print(request)

    # Check if the user exists with the provided email
    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "User not found",
            },
            status_code=404
        )
    
    # Verify the provided password with the stored hashed password
    if not bcrypt.verify(request.password, db_user.password):
        return JSONResponse(
            content={
                "status": False,
                "code": 401,
                "message": "Invalid password",
            },
            status_code=401
        )

    # Generate the JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    # Retrieve the UserDetails associated with this user
    db_user_details = db.query(UserDetails).filter(UserDetails.user_id == db_user.id).first()

    # If login is successful, return the JWT token along with user details
    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "data": {
                "id": db_user.id,
                "first_name": db_user.first_name,
                "last_name": db_user.last_name,
                "user_name": db_user.user_name,
                "email": db_user.email,
                "user_details": {
                    "address": db_user_details.address if db_user_details else None,
                    "state": db_user_details.state if db_user_details else None,
                    "city": db_user_details.city if db_user_details else None,
                    "zip_code": db_user_details.zip_code if db_user_details else None,
                },
                "created_at": db_user.created_at.strftime("%Y-%m-%dT%H:%M:%S") if db_user_details else None,
                "updated_at": db_user.updated_at.strftime("%Y-%m-%dT%H:%M:%S") if db_user_details else None,
            }
        },
        status_code=200
    )

# Function to decode and validate the JWT token
def decode_access_token(token: str):
    print(f"Token received: {token}")  # Debug print
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return email

@router.get("/protected-route")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}"}
