from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    role_id: int = Field(..., description="The role id of the user")
    first_name: str = Field(..., min_length=1, max_length=255, description="The first name of the user")
    last_name: str = Field(..., min_length=1, max_length=255, description="The last name of the user")
    user_name: str = Field(..., min_length=1, max_length=255, description="user name")
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., min_length=1, description="The password of the user")
    address: Optional[str] = Field(None, description="Address of the user")
    state: Optional[str] = Field(None, description="State of the user")
    city: Optional[str] = Field(None, description="City of the user")
    zip_code: Optional[str] = Field(None, description="Zip code of the user")
    
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., min_length=1, description="The password of the user")