from fastapi import FastAPI, APIRouter, HTTPException
from typing import Union
from enum import Enum

router = APIRouter()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class choice_names(str,Enum):
    one="one"
    two="two"
    three="three"

@router.get("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}

@router.get("/first_page")
def first_page_function():
    return "Hello my first page url"

# Path parameters
@router.get("/path_parameters/{item_id}", summary="Path parameters", description="Path parameters api")
async def read_item(item_id):
    return {"item_id": item_id}

@router.get("/path_parameters_with_types/{item_id}" , summary="Path parameters with types", description="Path parameters with types api")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.get("/products/{price}", summary="Path parameters with float types", description="Path parameters with float types")
async def read_product(price: float):
    return {"price": price, "message": f"The price is ${price:.2f}"}

@router.get("/student", summary="Path parameters with str, int types")
def student(name:str, roll_no:int):
    var_name = {"name": name , "roll number":roll_no}
    return (var_name)


@router.get("/enum_models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@router.get("/choice-function/{model_name}")
async def choiceFunction(model_name:choice_names):
    if model_name.value == "one":
        return {"model name": model_name, "message":"this is a one"}
    if model_name.value == "two":
        return {"model name": model_name, "message":"this is a two"}
    if model_name.value == "three":
        return {"model name": model_name, "message":"this is a three"}
    return model_name

@router.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# /////
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.get("/item/{id}")
def path_parameters(id):
    return {"get return id": id}


@router.get("/query_parameter/")
async def query_parameter(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@router.get("/query_optional_parameter/{item_id}")
async def query_optional_parameter(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Path parameters

@router.get("/items/{item_id}" , summary="Path parameters", description="Path parameters api", tags=["Path parameters"])
async def path_parameters_with_types(item_id: int):
    return {"item_id": item_id}

# Path parameters with types
@router.get("/items1/{item_id}", summary="Path parameters with int types", description="Path parameters with int types", tags=["Path parameters with types"])
async def read_item(item_id: int):
    return {"item_id": item_id, "description": f"Item {item_id}"}

@router.get("/users/{username}", summary="Path parameters with str types", description="Path parameters with str types", tags=["Path parameters with types"])
async def read_user(username: str):
    return {"username": username, "message": f"Hello, {username}!"}

# Path parameters with types with validation
@router.get("/itemsvalidation/{item_id}", summary="Path parameters with types with validation", description="Path parameters with types api with validation", tags=["Path parameters with types with validation"])
async def read_item_val(item_id: int):
    if item_id <= 5:  # Example of custom validation
        raise HTTPException(status_code=400, detail="Item ID must be greater than five.")
    return {"item_id": item_id, "description": f"Item {item_id}"}


@router.get("/query-optional-parameter")
def queryFunction(name:str, roll_no: Union[int, None]=None):
    var_name = {"name": name , "roll number":roll_no}
    return (var_name)