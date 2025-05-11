from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi import Depends
from typing import Optional
from typing import Union
from enum import Enum

router = APIRouter()


# Query Parameter with validation
@router.get("/query-parameters-with-validation/", description="Query Parameters with validation")
async def queryParametersWithValidation(name:str,age:int):
    return {"name": name, "age":age}

# Query Parameter without validation
@router.get("/query-parameters-without-validation/", description="Query Parameters without validation")
async def queryParametersWithoutValidation(name:str,age:int,roll_no = None, query: Union[str, None] = None, q: Optional[str]=None, short: bool = False):
    return {"name": name, "age":age, "roll_no":roll_no, "query":query, "short":short}
