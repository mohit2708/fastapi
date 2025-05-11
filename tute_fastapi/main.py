from fastapi import FastAPI, APIRouter, Depends, HTTPException, BackgroundTasks
from database.schemas.user import UserCreate
from database.models.user_details import UserDetails
from fastapi.responses import JSONResponse  # Include for message response.
from sqlalchemy.exc import SQLAlchemyError
from database.connection import get_db
from database.models.users import User
from database.models.roles import Role
from sqlalchemy.orm import Session
from typing import List
from fastapi import File, UploadFile

import bcrypt # for hashed password 


from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

from fastapi import Form
import os

# class EmailSchema:
#     def __init__(self, email: List[EmailStr], body: str):
#         self.email = email
#         self.body = body
    
class EmailSchema(BaseModel):
    email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME ="janicahanover@gmail.com",
    MAIL_PASSWORD = "dwglkfflvxoxzywr",
    MAIL_FROM = "janicahanover@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

# from dotenv import load_dotenv
# load_dotenv('.env')


# router = APIRouter()
app = FastAPI()

# @app.post("/send-email-with-attachment/")
# async def send_email_with_attachment(
#     background_tasks: BackgroundTasks,
#     file: UploadFile = File(...),
#     email: str = Form(...),
#     body: str = Form(...),
# ):
#     message = MessageSchema(
#         subject="Email with Attachment",
#         recipients=[email],
#         body=body,
#         subtype=MessageType.html,
#         attachments=[file.file],
#     )

#     background_tasks.add_task(fm.send_message, message)
#     return {"message": "Email has been sent"}



@app.post("/file")
async def send_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    email: EmailStr = Form(...)
) -> JSONResponse:
    try:
        # Read the file content
        file_content = await file.read()
        
        # Create the message
        message = MessageSchema(
            subject="FastAPI mail module",
            recipients=[email],
            body="Simple background task",
            subtype=MessageType.html,
            attachments=[{"filename": file.filename, "content": file_content}]
        )

        fm = FastMail(conf)

        # Add the task to the background tasks
        background_tasks.add_task(fm.send_message, message)

        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})
