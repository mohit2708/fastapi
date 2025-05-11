import os

from dotenv import load_dotenv
from typing import Dict
load_dotenv()

# class ProjectConfig:
#     PROJECT_NAME: str = os.getenv("PROJECT_NAME")
#     PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")

# project_config = ProjectConfig()

# class DbConfig:
#     POSTGRES_USER: str = os.getenv("POSTGRES_USER")
#     POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
#     POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
#     POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
#     POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
#     DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# db_config = DbConfig()

class JWTConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM =  os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    TOKEN_TYPE: str = "bearer"
    AUTH_HEADER: Dict[str,str] = {"WWW-Authenticate": "Bearer"}
    API_KEY_HEADER_NAME="ACCESS-TOKEN"

jwt_config = JWTConfig()