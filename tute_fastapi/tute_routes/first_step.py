from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}

@app.post("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}


@app.put("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}


@app.delete("/")
def first_page_function():
    return {"msg":"Hello FastAPI🚀"}

@app.get("/first_page")
def first_page_function():
    return "Hello my first page url"

@app.get("/items/{item_id}" , summary="Path parameters", description="Path parameters api", tags=["Path parameters"])
async def path_parameters_with_types(item_id: int):
    return {"item_id": item_id}