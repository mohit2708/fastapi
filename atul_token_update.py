from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.session import get_db
from core.hashing import HashData
from core.config import settings
from core.security import create_access_token
from core.constants import message
from database.repository.login import get_user
from schema.token import Token, TokenData, TokenCredentialIn,TokenOut
from schema.user import UserSchemaOut,BaseUserSchema
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.security import APIKeyHeader


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

header_scheme = APIKeyHeader(name=settings.API_KEY_HEADER_NAME)

router = APIRouter()

def authenticate_user(username,password,db):
    user = get_user(db,username)
    if not user:
        return False
    if not HashData.verify_password(password, user.hashed_password):
        return False    
    return user

async def get_current_user(token: Annotated[str, Depends(header_scheme)], db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentialsqqq",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:    
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        token_data = TokenData(email=email)
    except JWTError:
        return credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[UserSchemaOut, Depends(get_current_user)],
):
    #if current_user.disabled:
    #    raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@router.post("/login",response_model=TokenOut, response_class=JSONResponse,name="login")
async def login_for_access_token(credentials: TokenCredentialIn,db:Session = Depends(get_db)):
    try: 
        user = authenticate_user(credentials.email, credentials.password,db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message.INCORRECT_CREDENTIALS,
                headers=settings.AUTH_HEADER
            )
        access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"email": user.email}, expires_delta=access_token_expires
        )
        http_status_code = 200
        user_data = {
            "status_code": http_status_code,
            "status":True,
            "access_token":access_token,
            "token_type":settings.TOKEN_TYPE,
            "first_name": user.first_name,
            "email": user.email,
            "role": user.role,
            "country":user.country,
            "state":user.state,
            "city":user.city,
            "address":user.address,
            "zeep_code":user.zeep_code
        }
        response_data = TokenOut(**user_data)
        response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
    #return Token(access_token=access_token, token_type=settings.TOKEN_TYPE)
    except ValueError as e:
        http_status_code = 500
        error_detail = f"Invalid response data: {e}"
        response_data = {
            "status_code": http_status_code,
            "status": False,
            "detail": error_detail
        }
        response = JSONResponse(content=response_data, status_code=http_status_code)
    return response
    
@router.get("/users/me/", response_model=UserSchemaOut)
async def read_users_me(current_user: Annotated[UserSchemaOut, Depends(get_current_active_user)]):
    http_status_code: int = 200
    status:bool = True
    data = {"first_name":current_user.first_name,"last_name":current_user.last_name,"email":current_user.email,"username":current_user.username,"role":current_user.role,"country":current_user.country,"state":current_user.state,"city":current_user.city,"address":current_user.address,"zeep_code":current_user.zeep_code,"status_code":http_status_code,"status":status}
    response_data = UserSchemaOut(**data)
    response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
    return response


@router.get("/test")
async def read_users_me():
    return "hello"