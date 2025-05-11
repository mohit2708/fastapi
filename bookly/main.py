from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def hello():
    return {"msg":"fastapi"}

@app.get('/greet/{name}')
async def greet(name:Optional[str]="mohit", age:int=0) -> dict:
    return {"hello":f"hello {name}, and age {age}"}
