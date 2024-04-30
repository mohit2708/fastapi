from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.orm import Session
from database.models.user import User
from database.models.role import Role
from database.schemas.user import UserCreate
from sqlalchemy.exc import IntegrityError

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from database.connection import get_db
import bcrypt # for hashed password
from passlib.context import CryptContext
from database.schemas.token import Token, TokenData, TokenCredentialIn,TokenOut



router = APIRouter()


@router.post("/login1")
async def login_for_access_token(credentials: TokenCredentialIn,db:Session = Depends(get_db)):
    getuser = get_user(credentials.email, credentials.password,db)
    print(getuser)
    # if not user:
    #     return False
    # if not verify_password(password, user.hashed_password):
    #     return False    
    # return user



@staticmethod 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)    



'''
list user
'''

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session = Depends(get_db)):
    print(form_data)
    user = authenticate_user(form_data.username, form_data.password,db)
    pass

@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# def create_new_user(user: UserCreate, db: Session):
#     try:
#         db_user = User(**user.dict())
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user
#     except IntegrityError as e:
#         db.rollback()
#         error_message = "Email already exists."
#         return {"detail": error_message}



# @router.post("/user/add")
# def add(user: UserCreate, db1: Session = Depends(get_db)):
#     user = create_new_user(user=user, db=db1)
#     return user 