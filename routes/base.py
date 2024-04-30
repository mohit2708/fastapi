from fastapi import APIRouter

from routes import routes_basic
from routes import routes_pathparameter
from routes import routes_queryparameters
from routes import routes_bodyparameter
from routes import route_role
from routes import route_user
from routes import route_auth



api_router = APIRouter()

api_router.include_router(routes_basic.router,prefix="",tags=["Basic Routes"])
api_router.include_router(routes_pathparameter.router,prefix="",tags=["Path Parameter Routes"])
api_router.include_router(routes_queryparameters.router,prefix="",tags=["Query Parameters"])
api_router.include_router(routes_bodyparameter.router,prefix="",tags=["Body Parameter Routes"])
api_router.include_router(route_role.router,prefix="",tags=["Role Routes"])
api_router.include_router(route_auth.router,prefix="",tags=["Auth Routes"])
api_router.include_router(route_user.router,prefix="",tags=["User Routes"])