from fastapi import FastAPI, Query
from typing import Optional
from typing import Annotated


app = FastAPI()


@app.get("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}

fake_items_db = [{"item_name": "A"}, {"item_name": "B"}, {"item_name": "C"}, {"item_name": "D"}]


@app.get("/items/", summary="Query parameters", description="Query parameters api", tags=["Query parameters"])
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/query_parameters_ptional/{item_id}", summary="Query parameters Optional without package" , description="Query parameters Optional" , tags=["Query parameters Optional"])
async def query_parameters_ptional(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/query_parameters_ptional1/{item_id}", summary="Query parameters Optional with package" , description="Query parameters Optional" , tags=["Query parameters Optional"])
async def query_parameters_ptional1(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.get("/bool/{item_id}")
async def bool(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Query parameters with validation

@app.get("/string_validation/" , summary="Query parameters with string validation" , tags=["Query parameters with validation"])
async def string_validation(name:str, q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/int_validation/" , summary="Query parameters with int validation" , tags=["Query parameters with validation"])
async def int_validation(q: int | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/length_validation/"  , summary="Query parameters with length validation" , tags=["Query parameters with validation"])
async def length_validation(q: Annotated[str | None, Query(max_length=3)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/length_validation2/" , summary="Query parameters with length validation" , tags=["Query parameters with validation"])
async def length_validation2(q: str | None = Query(default=None, max_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/max_min_length_validation/" , summary="Query parameters with length validation min_length max_length" , tags=["Query parameters with validation"])
async def max_min_length_validation(q: Annotated[str | None, Query(min_length=3, max_length=5)] = None,):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/pattern_validation/" , summary="Query parameters with pattern validation" , tags=["Query parameters with validation"])
async def pattern_validation(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None,):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

@app.get("/list_multipal_value/", summary="Query parameters list / multiple values" , tags=["Query parameters with validation"])
async def list_multipal_value(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items


@app.get("/ellipsis/" , tags=["Query parameters with Ellipsis"])
async def ellipsis(q: Annotated[str, Query(min_length=3)] = ...):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Ques.
# 1. pattern validation
# 2. Query Parameters and String Validations  ->   Required with Ellipsis (...)
