from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import Depends
from typing import Optional
from typing import Union
from enum import Enum

router = APIRouter()


# Path Parameter
@router.get("/user/{user_name}", description="Path Parameters without Types")
def userName(user_name):
    return {"user name": user_name}

# Path Parameters with Types
@router.get("/user/{name}/{age}", description="Path Parameters with Types")
async def pathParametersWithTypes(name:str,age:int):
    return {"name": name, "age":age, "message": f"my name is {name} and my age is {age}!"}





class foodEnum(str, Enum):
    fruits = "fruits"
    vagitable = "Vagitable"
    dairy = "Dairy"

@router.get("/foods/{food_name}")
def getFoods(food_name:foodEnum):
    if food_name == foodEnum.vagitable:
        return {"food_name": food_name }
    if food_name == foodEnum.fruits:
        return{
            "food_name": food_name
        }
    else:
        return{
            "food_name": food_name
        }

fake_item_db = [{"item_name":"Foo"},{"item_name":"asdgf"},{"item_name":"Foqwro"},{"item_name":"Fozxvo"}]

@router.get("/items/fake_item_db")
def list_items(skip:int = 0, limit:int = 10):
    return fake_item_db[skip : skip + limit]

@router.get("/items/{item_id}")
def get_item(item_id, q: Optional[str]=None, short: bool = False):
# def get_item(item_id, q:str | None = None):
    item = {"item_id": item_id}
    if q:
        item.update( {"item_id":item_id, "q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@router.get("/user/{user_id}/items/{item_id}")
async def multipal_parameter(user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id":user_id}
    if q:
        item.update( {"q":q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

