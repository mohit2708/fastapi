from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.get("/users", tags=["authentication"])
async def read_user():
    pass