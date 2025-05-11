from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str = "Mohit saxena"
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/", tags=["Request Body"])
async def create_item(item: Item):
    return item

@app.post("/some_logic/" , tags=["Request Body"])
async def some_logic(item: Item):
    item_dict = item.dict()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# Request body + path parameters
@app.put("/items/{item_id}", tags=["Request body + path parameters"])
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Request body + path + query parameters
@app.put("/req_body_path_query_parameters/{item_id}" , tags=["Request body + path + query parameters"])
async def req_body_path_query_parameters(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


############## item.dict()
# In the context of the FastAPI framework, the item.dict() method is used to convert a Pydantic model instance (in this case, item) into a dictionary. 
###################### **item.dict()
# In Python, the ** operator is used for unpacking dictionaries. When you see **item.dict(), 
# it means that the key-value pairs from the dictionary returned by item.dict() are being unpacked and included in the new dictionary being created.
#########################

