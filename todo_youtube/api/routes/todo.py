from fastapi import APIRouter

todo_router = APIRouter(prefix="/api", tags=["Todo"])

@todo_router.get("/")
def all_todos():
    return {"sadf"}


@todo_router.post("/")
def post_todos():
    return {"sadf"}


@todo_router.put("/{key}")
def put_todos(key:int):
    return {"sadf"}

@todo_router.delete("/{key}")
def delete_todos(key:int):
    return {"sadf"}