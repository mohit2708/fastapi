from typing import Union
from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class choice_names(str,Enum):
    one="one"
    two="two"
    three="three"
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}

@app.get("/first_page")
def first_page_function():
    return "Hello my first page url"

@app.get("/item/{id}")
def path_parameters(id):
    return {"get return id": id}


@app.get("/query_parameter/")
async def query_parameter(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/query_optional_parameter/{item_id}")
async def query_optional_parameter(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

# Path parameters

@app.get("/items/{item_id}" , summary="Path parameters", description="Path parameters api", tags=["Path parameters"])
async def path_parameters_with_types(item_id: int):
    return {"item_id": item_id}

# Path parameters with types
@app.get("/items1/{item_id}", summary="Path parameters with int types", description="Path parameters with int types", tags=["Path parameters with types"])
async def read_item(item_id: int):
    return {"item_id": item_id, "description": f"Item {item_id}"}

@app.get("/users/{username}", summary="Path parameters with str types", description="Path parameters with str types", tags=["Path parameters with types"])
async def read_user(username: str):
    return {"username": username, "message": f"Hello, {username}!"}

@app.get("/products/{price}", summary="Path parameters with float types", description="Path parameters with float types", tags=["Path parameters with types"])
async def read_product(price: float):
    return {"price": price, "message": f"The price is ${price:.2f}"}

# Path parameters with types with validation
@app.get("/itemsvalidation/{item_id}", summary="Path parameters with types with validation", description="Path parameters with types api with validation", tags=["Path parameters with types with validation"])
async def read_item_val(item_id: int):
    if item_id <= 5:  # Example of custom validation
        raise HTTPException(status_code=400, detail="Item ID must be greater than five.")
    return {"item_id": item_id, "description": f"Item {item_id}"}

@app.get("/query")
def queryFunction(name:str, roll_no:int):
    var_name = {"name": name , "roll number":roll_no}
    return (var_name)

@app.get("/query-optional-parameter")
def queryFunction(name:str, roll_no: Union[int, None]=None):
    var_name = {"name": name , "roll number":roll_no}
    return (var_name)

@app.get("/choice-function/{model_name}")
async def choiceFunction(model_name:choice_names):
    if model_name.value == "one":
        return {"model name": model_name, "message":"this is a one"}
    if model_name.value == "two":
        return {"model name": model_name, "message":"this is a two"}
    if model_name.value == "three":
        return {"model name": model_name, "message":"this is a three"}
    return model_name