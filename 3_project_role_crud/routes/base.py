from fastapi import APIRouter

from routes import route_role
from routes import user

api_router = APIRouter()

api_router.include_router(route_role.router,prefix="",tags=["Role Routes"])
api_router.include_router(user.router,prefix="",tags=["User Routes"])
