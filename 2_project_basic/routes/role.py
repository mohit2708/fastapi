from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/role-list/")
def get_roles_list():
    return {"msg":"get role list🚀"}
