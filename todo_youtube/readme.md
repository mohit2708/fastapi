* activate enviroment

### Insatall packages
* fastapi


* create app folder and create main.py file
```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {"message": "first route"}
```

* create main.py file in root folder
```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
```

* run cmd in cmd 
```python
python main.py
```


### step2
* create the api folder -> create route folder and __init__ .py and todo.py file
* 