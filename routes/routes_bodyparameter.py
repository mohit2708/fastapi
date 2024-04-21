from typing import Optional, Union, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import Depends
from enum import Enum
from fastapi import HTTPException

router = APIRouter()

class Student(BaseModel):
   id: int
   name :str = Field(None, title="name of student", max_length=10)
   subjects: List[str] = []

@router.post("/students/")
async def student_data(s1: Student):
    try:
        return s1
    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid input: " + str(ve))


class Item(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    tax : Union[float, None] = None

@router.post("/items")
async def create_items(item: Item):
    # return item
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict



# import uvicorn
# from fastapi import FastAPI

# from pydantic import BaseModel, Field
# app = FastAPI()