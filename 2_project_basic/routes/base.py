from fastapi import APIRouter

from routes import role
from routes import user

api_router = APIRouter()

api_router.include_router(role.router,prefix="",tags=["Role Routes"])
api_router.include_router(user.router,prefix="",tags=["User Routes"])
