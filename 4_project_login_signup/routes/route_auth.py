from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models.users import User
from database.models.roles import Role

from fastapi.responses import JSONResponse  # Include for message response.
from sqlalchemy.exc import SQLAlchemyError

from database.schemas.user import UserCreate, UserLogin

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
    
    db_user = User(
            role_id=request.role_id,
            first_name=request.first_name,
            last_name=request.last_name,
            user_name=request.user_name,
            email=request.email,
            password=request.password  # Store the hashed password as string
        )

    # db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
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
                "created_at": db_user.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                "updated_at": db_user.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
            }
        },
        status_code=200
    )