### **Create virtual enviroment**
* create the folder and open the cmd
```python
python -m venv virtual-name
OR
pip install virtualenv  # Install the package.
virtualenv MyFirstApp
MyFirstApp\scripts\activate
```

#### **Activated virtual enviroment**
```pyhton
cd virtual-name\Scripts
d:\mohit\virtual-name\Scripts> activate
```

### install fastapi
* we have install two packages/library **fastapi** and **uvicorn**
```python
pip install "fastapi[all]" uvicorn[standard] sqlalchemy PyMySQL

pip install fastapi

# You will also need an ASGI server, for production such as Uvicorn or Hypercorn.
pip install "uvicorn[standard]"
```

### create the requiments file.
```python
pip freeze > requirements.txt
```

### Create a file main.py with:
```python
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/first_page/")
def first_page_function():
    return "Hello my first page url"
```

### Run the server with:
```python
uvicorn main:app --reload

uvicorn main:app --host 127.8.4.8 --port 12   # Difrent port

# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [28720]
# INFO:     Started server process [28722]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```
```python
Open your browser at http://127.0.0.1:8000/docs
Open your browser at http://127.0.0.1:8000/items
```

### Create the env file
* install the package
```python
pip install python-dotenv
```
* creaet the .env file in root folder
```python
PROJECT_NAME    = "Mohit API's. 🔥"
PROJECT_VERSION = "1.0.0"
```
* call in main.py file
```python
import os
from typing import Union
from pathlib import Path
from fastapi import FastAPI
from dotenv import load_dotenv

# load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# app = FastAPI()
app = FastAPI(title=os.getenv("PROJECT_NAME"),version=os.getenv("PROJECT_VERSION"))
```

### Databse Connection
* Install sqlalchemy
```python
pip install sqlalchemy
```
```python
pip install PyMySQL
```
* add code in .env file
```python
MY_SQL_USER=root
MY_SQL_PASSWORD=
MY_SQL_SERVER=localhost
MY_SQL_PORT=
MY_SQL_DATABASE=profile_fastapi
```
* Create the connection.py
```python
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

MY_SQL_USER     = os.getenv("MY_SQL_USER")
MY_SQL_SERVER   = os.getenv("MY_SQL_SERVER")
MY_SQL_PASSWORD = os.getenv("MY_SQL_PASSWORD")
MY_SQL_PORT     = os.getenv("MY_SQL_PORT")
MY_SQL_DATABASE = os.getenv("MY_SQL_DATABASE")

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/profile_fastapi"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{MY_SQL_USER}:@{MY_SQL_SERVER}/{MY_SQL_DATABASE}"

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:   #new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
```

### Install alembic
* install package
```python
pip install alembic
```
* Initialize Alembic:
```python
alembic init alembic
```
#####  Change code in alembic.py 
```python
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = mysql+pymysql://root:@localhost/profile_fastapi
```

##### Change code in env.py file under the alembic folder
```python

from database.connection import Base

from database.models import *
target_metadata = Base.metadata
```


### create Model structure
* Create the databse folder
* create the model folder
* Create the user.py, role.py and init.py file
```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))  # Define foreign key relationship
    role = relationship("Role", back_populates="users")  # Define relationship with Role model
    first_name = Column(String(255))
    last_name = Column(String(255))
    user_name = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    zip_code = Column(String(255))
    is_active = Column(Boolean(), default=True)
    address = Column(String(255))
    country = Column(Integer)
    state = Column(Integer)
    city = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database.connection import Base

class Role(Base):
    __tablename__ = "roles"

    id          = Column(Integer, primary_key=True, index=True)
    slug        = Column(String(255), nullable=True)
    name        = Column(String(255), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    users = relationship("User", back_populates="role")  # Define reverse relationship with User model
```


* create the **base.py** file and **base_class.py** file
```python
# base.py
from database.models.base_class import Base
from database.models.roles import Role
from database.models.users import User
from database.models.customers import Customer
```
```python
# base_class.py
from typing import Any
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

@as_declarative()
class Base:
    id: Any
    __name__: str

    #to generate tablename from classname
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
```

### Genrate alembic
```python
alembic revision --autogenerate -m "create user and blog table migrations"  #analyzes tables and creates a migration file
```
```python
alembic upgrade head  #executes the migration files to make actual changes in db
```


### Create table into databse
* add some code
```python
# main.py
from database.connection import engine
from database.models.base import Base

def create_tables():
	Base.metadata.create_all(bind=engine)
```



### JWT
```python
pip install "python-jose[cryptography]"
```
```python
pip install "passlib[bcrypt]"
```
```python
pip install python-multipart
```


## Create User
### Hash Password
* Using bcrypt
```python
import bcrypt # for hashed password

@router.post("/users/add")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": "Email already registered",
            },
            status_code=400
        )

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    hash_password = hashed_password.decode('utf-8')

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        user_name=user.user_name,
        email=user.email,
        password=hash_password  # Store the hashed password as string
    )

    # db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```
* Using passlib
```python
from passlib.context import CryptContext

@router.post("/users/add")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": "Email already registered",
            },
            status_code=400
        )
    # Hash the password before storing it
    pwd_hashed = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_hashed.hash(user.password)
    

    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        user_name=user.user_name,
        email=user.email,
        password=hashed_password  # Store the hashed password as string
    )

    # db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```
