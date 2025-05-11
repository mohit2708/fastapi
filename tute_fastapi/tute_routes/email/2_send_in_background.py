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


import bcrypt # for hashed password 


from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List

class EmailSchema(BaseModel):
    email: List[EmailStr]
    # email: str
    


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

@app.post("/send_in_background")
async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema
    ) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=email.dict().get("email"),
        body="Simple background task",
        subtype=MessageType.plain)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message,message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
