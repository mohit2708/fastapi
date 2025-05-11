from pydantic import BaseModel, field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator

GetTodo = pydantic_model_creator(None, name="Todo")

class PostTodo(BaseModel):
    task:str = field(..., max_length=100)
    doon:bool

class PutTodo(BaseModel):
    task:Optional[str] = field(..., max_length=100)
    doon:Optional[bool]
