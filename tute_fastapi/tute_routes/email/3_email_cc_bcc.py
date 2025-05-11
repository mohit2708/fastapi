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

app = FastAPI()

@app.post("/simple_send_with_function_cc_bcc")
async def simple_send_with_function_cc_bcc(email: EmailSchema, background_tasks: BackgroundTasks):
    body = """<h1>Your have successfully Test</h1> """
    subject = "Your have successfully login"
    # toemail = [email.email]
    toemail = email.email
    ccemail = ['mksaxena27@yopmail.com']
    bccemail = ['mksaxena2708@yopmail.com']
    # ccemail = ['atulcc@yopmail.com', 'anothercc@yopmail.com']  # List of CC email addresses
    # bccemail = ['atulbcc@yopmail.com', 'anotherbcc@yopmail.com']  # List of BCC email 
    emailBody = body
    send_email(background_tasks=background_tasks,emaiSubject=subject,emailTo=toemail,emailBody=emailBody,ccemail=ccemail,bccemail=bccemail)

# request in fastapi
# {
#   "email": [
#     "mksaxena27@yopmail.com",
#     "mksaxena08@yopmail.com"
#   ]
# }

def send_email(background_tasks, emaiSubject, emailTo, emailBody, ccemail=[], bccemail=[]):
    fm = FastMail(conf)
    mailData = MessageSchema(
        subject=emaiSubject,
        recipients=emailTo,  # Pass the list of email addresses directly
        cc=ccemail,
        bcc=bccemail,
        body=emailBody,
        subtype=MessageType.html
    )
    background_tasks.add_task(fm.send_message, mailData)


