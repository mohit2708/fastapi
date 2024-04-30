from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.orm import Session
from database.models.user import User
from database.models.role import Role
from database.schemas.user import UserCreate, UserLogin
from sqlalchemy.exc import IntegrityError

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from database.connection import get_db
import bcrypt # for hashed password
from passlib.context import CryptContext
from database.schemas.token import Token, TokenData, TokenCredentialIn,TokenOut
from datetime import datetime, timedelta, timezone
from core.config import jwt_config


router = APIRouter()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

'''
Create user
role id exist or not
username or email already exist
password hash
'''
@router.post("/registration")
def registration_user(request: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user_username = User.get_user_by_username(db, request)
        existing_user_email = User.get_user_by_email(db, request)

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

        # db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Something Went Wrong!!")



@router.post("/login/")
async def login(request: UserLogin, db: Session = Depends(get_db)):
    user = User.get_user_by_email(db, request)
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    if not User.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    # Here you can generate and return a JWT token for authentication if needed
    return {"message": "Login successful"}





# @router.post("/login", response_model=TokenOut, response_class=JSONResponse, name="login")
# async def login_user(request: TokenCredentialIn, db:Session = Depends(get_db)):
#     user = db.query(User).filter(User.email == request.email).first()
#     # if not user: OR
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    
#     hashed_pass = user.password
#     if not verify_password(request.password, hashed_pass):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect password"
#         )
#     print(jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token_expires = timedelta(minutes=int(jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES))
#     return access_token_expires


    #     access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    #     access_token = create_access_token(
    #         data={"email": user.email}, expires_delta=access_token_expires
    #     )
    #     http_status_code = 200
    #     user_data = {
    #         "status_code": http_status_code,
    #         "status":True,
    #         "access_token":access_token,
    #         "token_type":settings.TOKEN_TYPE,
    #         "first_name": user.first_name,
    #         "email": user.email,
    #         "role": user.role,
    #         "country":user.country,
    #         "state":user.state,
    #         "city":user.city,
    #         "address":user.address,
    #         "zeep_code":user.zeep_code
    #     }
    #     response_data = TokenOut(**user_data)
    #     response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
    # return response



# from fastapi import APIRouter, Depends, HTTPException
# from jose import jwt
# from datetime import datetime, timedelta
# from .models import User
# from .database import SessionLocal
# from .config import SECRET_KEY

# router = APIRouter()

# # Function to blacklist tokens
# blacklisted_tokens = set()

# def is_token_blacklisted(token: str):
#     return token in blacklisted_tokens

# def invalidate_token(token: str):
#     blacklisted_tokens.add(token)

# @router.post("/logout/")
# async def logout(token: str = Depends(get_token)):
#     if is_token_blacklisted(token):
#         raise HTTPException(status_code=400, detail="Token already invalidated")
#     else:
#         invalidate_token(token)
#         return {"message": "Logged out successfully"}
