from pydantic import BaseModel, Field
from typing import List, Any

class RoleCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=6, description="The slug of the role")
    name: str = Field(..., min_length=1, max_length=6, description="The name of the role")

class RoleUpdate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=10, description="The slug of the role")
    name: str = Field(..., min_length=1, max_length=10, description="The name of the role")

    class Config:
        from_attributes = True