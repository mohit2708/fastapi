from fastapi import FastAPI
import  models
from database import SessionLocal, engine

from routes.accounts import auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth.auth_router)

@app.get("/hello")
def hello_word():
    return "hello word"