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
from schema.token import Token, TokenData
from schema.user import UserSchemaOut,BaseUserSchema
from fastapi.responses import JSONResponse, ORJSONResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()

def authenticate_user(username,password,db):
    user = get_user(db,username)
    if not user:
        return False
    if not HashData.verify_password(password, user.hashed_password):
        return False    
    return user



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
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



@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session = Depends(get_db))->Token:
    user = authenticate_user(form_data.username, form_data.password,db)
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
    return Token(access_token=access_token, token_type=settings.TOKEN_TYPE)


    
@router.get("/users/me/", response_model=UserSchemaOut)
async def read_users_me(current_user: Annotated[UserSchemaOut, Depends(get_current_active_user)]):
    http_status_code: int = 200
    status:bool = True
    data = {"first_name":current_user.first_name,"last_name":current_user.last_name,"email":current_user.email,"username":current_user.username,"role":current_user.role,"country":current_user.country,"state":current_user.state,"city":current_user.city,"address":current_user.address,"zeep_code":current_user.zeep_code,"status_code":http_status_code,"status":status}
    response_data = UserSchemaOut(**data)
    response = JSONResponse(content=response_data.dict(),status_code=http_status_code)
    return response