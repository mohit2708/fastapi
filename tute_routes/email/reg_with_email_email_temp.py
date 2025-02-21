from fastapi import FastAPI, APIRouter, Depends, HTTPException, BackgroundTasks
from database.schemas.user import UserCreate
from database.models.user_details import UserDetails
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from database.connection import get_db
from database.models.users import User
from database.models.roles import Role
from sqlalchemy.orm import Session
from typing import List

import bcrypt  # for hashed password

from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
import os

class EmailSchema(BaseModel):
    email: List[EmailStr]
    # email: str

conf = ConnectionConfig(
    MAIL_USERNAME="janicahanover@gmail.com",
    MAIL_PASSWORD="dwglkfflvxoxzywr",
    MAIL_FROM="janicahanover@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

app = FastAPI()

# @app.post("/pathcheck")
# async def pathcheck():
#     html_file_path = os.path.join(os.path.dirname(__file__), 'templates', 'email_template.html')
#     return html_file_path


@app.post("/registration_user_with_send_email")
async def registration_user_with_send_email(request: UserCreate, db: Session = Depends(get_db)):
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
        password=hash_password  # Store the hashed password as string
    )

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

    # Read the HTML template file
    html_file_path = os.path.join(os.path.dirname(__file__), 'templates', 'email.html')
    with open(html_file_path, 'r') as file:
        html_template = file.read()

    # Render the HTML template with the user's first name
    html = html_template.format(first_name=request.first_name)

    # Send email to the registered user
    message = MessageSchema(
        subject="Welcome to Our Service",
        recipients=[request.email],  # Use a list of email addresses
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)

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