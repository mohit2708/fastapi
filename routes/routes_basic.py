from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()

@router.get("/")
async def root():
    return {"message": f"Hello, welcome to!"}

@router.post("/")
async def post():
    return {"message": f"Hello, from the post route!"}

@router.put("/")
async def put():
    return {"message": f"Hello, from the put route!"}

@router.get("/first_page/", description="This is first api", deprecated=True,name="firstname")
def first_page_function():
    return "Hello my first page url"

@router.get("/blog/list")
def index():
    return "showing the user list"

@router.post("/blog/add")
def add():
    return "showing the user list"
