from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/user-list/")
def get_user_list():
    return {"msg":"get user list🚀"}