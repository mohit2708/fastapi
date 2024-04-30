from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class TokenCredentialIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    status_code: Optional[int] = None
    status: Optional[bool] = None
    access_token: str
    token_type: str
    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    username: Optional[str] = None
    role: int
    country: int
    state: int
    city: int
    address: Optional[str] = None
    zeep_code: Optional[str] = None
