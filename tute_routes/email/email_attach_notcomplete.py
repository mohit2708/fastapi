from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
import os

class EmailSchema(BaseModel):
    email: List[EmailStr]
    attachments: List[str] = []  # List of file paths for attachments

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

@app.post("/emailbackground")
async def send_in_background(
    background_tasks: BackgroundTasks,
    email: EmailSchema
) -> JSONResponse:
    # Read the image content and prepare the attachments
    attachments = []
    for file_path in email.attachments:
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                file_content = file.read()
                file_name = os.path.basename(file_path)  # Get the base name of the file
                attachments.append({"file": file_name, "content": file_content})
        else:
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

    message = MessageSchema(
        subject="Fastapi mail module",
        recipients=email.dict().get("email"),
        body="Simple background task with image attachment",
        subtype=MessageType.plain,
        attachments=attachments  # Add the attachments here
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})



# {
#   "email": [
#     "mksaxena27@yopmail.com"
#   ],
#   "attachments": ["D:/gitOcean/public/uploads/profile/20240930_112754_HD-wallpaper-lord-shiva-artwork-others.jpg"]
# }
