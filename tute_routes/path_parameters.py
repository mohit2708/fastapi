from fastapi import FastAPI, Path, Query
from typing import Annotated
from enum import Enum


app = FastAPI()


@app.get("/path_parameters/{item_id}" , tags=["Path parameters"])
async def path_parameters(item_id):
    return {"item_id": item_id}



@app.get("/path_parameters_with_int_validation/{item_id}" , tags=["Path parameters with validation"])
async def path_parameters_with_int_validation(item_id:int):
    return {"item_id": item_id}


@app.get("/path_parameters_with_str_validation/{user_id}", tags=["Path parameters with validation"])
async def path_parameters_with_str_validation(user_id: str):
    return {"user_id": user_id}

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}" , tags=["Path parameters with Predefined values (Enum)"])
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/items/{item_id}", tags=["Path parameters with Predefined values (Enum)"])
async def read_items(item_id: Annotated[int, Path(title="The ID of the item to get")],q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/items1/{item_id}")
async def read_items1(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results  


@app.get("/items2/{item_id}")
async def read_items2(*, item_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# gt: greater than
# ge: greater than or equal
# lt: less than
# le: less than or equal


@app.get("/greater_than_or_equal/{item_id}" , tags=["greater than/greater than or equal/less than/less than or equal"])
async def greater_than_or_equal(item_id: Annotated[int, Path(title="The ID of the item to get", ge=5)], q: str):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results



@app.get("/greater_than_and_less_than_or_equal/{item_id}", tags=["greater than/greater than or equal/less than/less than or equal"])
async def greater_than_and_less_than_or_equal(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=5, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results