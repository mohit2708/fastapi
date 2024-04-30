# from typing import List, Union



# class ItemBase(BaseModel):
#     title: str
#     description: Union[str, None] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         from_attributes = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True

# ====================================

from pydantic import BaseModel, Field
from typing import List, Any

class RoleCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=6, description="The slug of the role")
    name: str = Field(..., min_length=1, max_length=6, description="The name of the role")

    # class Config:
    #     alias_generator = lambda field_name: field_name
    #     allow_population_by_field_name = True
    #     error_msg_templates = {
    #         'string_too_short': 'Field "{field}" is required.'
    #     }



class RoleList(BaseModel):
    success: bool
    code: int
    message: str
    roles: List[Any]
    # roles: List[dict]
    

    class Config:
        from_attributes = True

class RoleDetail(BaseModel):
    id: int
    slug: str
    name: str

    class Config:
        # orm_mode = True
        from_attributes = True

class RoleUpdate(BaseModel):
    slug: str
    name: str = Field(..., min_length=1, max_length=255, description="The name of the role")

    class Config:
        from_attributes = True


class RoleDelete(BaseModel):
    id: int
    slug: str
    name: str

    class Config:
        from_attributes = True