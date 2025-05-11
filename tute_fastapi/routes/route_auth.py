from fastapi import FastAPI, APIRouter, Depends, HTTPException
from database.schemas.user import UserCreate, UserLogin
from database.models.user_details import UserDetails
from fastapi.responses import JSONResponse  # Include for message response.
from sqlalchemy.exc import SQLAlchemyError
from database.connection import get_db
from database.models.users import User
from database.models.roles import Role
from sqlalchemy.orm import Session

import bcrypt # for hashed password 

router = APIRouter()

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
    hash_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db_user = User(
            role_id=request.role_id,
            first_name=request.first_name,
            last_name=request.last_name,
            user_name=request.user_name,
            email=request.email,
            # password=request.password
            password=hash_password  # Store the hashed password as string
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
@router.post("/login_user")
def login_user(request: UserLogin, db: Session = Depends(get_db)):

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
    if not bcrypt.checkpw(request.password.encode('utf-8'), db_user.password.encode('utf-8')):
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