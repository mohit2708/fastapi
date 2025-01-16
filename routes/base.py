from fastapi import APIRouter

from routes import routes_1_path_parameters
from routes import routes_2_bodyparameter
from routes import routes_3_queryparameters
from routes import route_2_role
from routes import route_auth
from routes import user
from routes import route_send_email_during_registraion
from routes import route_login_jwt


# from routes import route_login_jwt_fastapi_example


# from routes import user

api_router = APIRouter()

api_router.include_router(route_2_role.router,prefix="",tags=["Role Routes"])
api_router.include_router(route_auth.router,prefix="",tags=["Login and signup Routes"])
api_router.include_router(route_login_jwt.router,prefix="",tags=["Login with jwt"])
# api_router.include_router(route_login_jwt_fastapi_example.router,prefix="",tags=["jwts authonicate example fastapi"])
api_router.include_router(route_send_email_during_registraion.router,prefix="",tags=["Email Send during Registration"])
api_router.include_router(user.router,prefix="",tags=["User Routes"])
api_router.include_router(routes_1_path_parameters.router,prefix="",tags=["Path Parameters"])
api_router.include_router(routes_2_bodyparameter.router,prefix="",tags=["Body Parameters"])
api_router.include_router(routes_3_queryparameters.router,prefix="",tags=["query Parameters"])


