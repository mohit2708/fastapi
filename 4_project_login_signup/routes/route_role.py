from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db

from database.models.roles import Role

from fastapi.responses import JSONResponse  # Include for message response.

from database.schemas.role import RoleCreate, RoleUpdate
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.get("/role-list/")
def get_roles_list(db: Session = Depends(get_db)):
    roles = db.query(Role.id, Role.slug, Role.name).all()
    
    '''
    Check Role list is empty or not
    '''
    if not roles:  # Check if the roles list is empty
        return JSONResponse(
            content={
                "success": True,
                "code": 200,
                "message": "Role list is empty",
            },
            status_code=200
        )
    '''
    Get Role Data
    '''
    roles_list = []
    for role in roles:
        role_dict = {
            "id": role.id,
            "slug": role.slug,
            "name": role.name
        }
        roles_list.append(role_dict)
    return JSONResponse(
        content={
            "success": True,
            "code": 200,
            "message": "Roles list retrieved successfully",
            "data": roles_list
        },
        status_code=200  # You can change this to any valid HTTP status code
    )
    # return {
    #     "success": True,
    #     "code": 200,
    #     "message": "Roles list retrieved successfully",
    #     "data": roles_list
    # }

'''
Get role List by id
'''
@router.get("/role/{role_id}")
def get_role_list_by_id(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    # if not role:
    if role is None:
        # raise HTTPException(status_code=404, detail="Role not found")
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": f"Role id {role_id} does not exists!!"
            },
            status_code=400
        )
    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "Role retrieved successfully!",
            "data": {
                "id": role.id,
                "slug": role.slug,
                "name": role.name
            }
        },
        status_code=200
    )

'''
Create Role Data
'''
@router.post("/role/create")
# def create_role_handler(slug: str,name:str, db: Session = Depends(get_db)):
def create_role_handler(role: RoleCreate, db: Session = Depends(get_db)):  # input field from the RoleCreate scheme
    try:
        existing_role = db.query(Role).filter(Role.slug == role.slug).first()
        if existing_role:
            return JSONResponse(
                content={
                    "status": False,
                    "code": 400,
                    "message": "Role with this slug already exists"
                },
                status_code=400
            )
        
        new_record = Role(**role.dict())
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return JSONResponse(
            content={
                "status": True,
                "code": 200,
                "message": "Role has been created successfully!",
                "data": {
                    "id": new_record.id,
                    "slug": new_record.slug,
                    "name": new_record.name,
                    "created_at": new_record.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                    "updated_at": new_record.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
                }
            },
            status_code=200
        )


    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

'''
Update Role data by id
'''
@router.put("/role/{role_id}/update", response_model=RoleUpdate)
def update_role_handler(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):

    '''
    Check Role id exist or not
    '''
    get_role_id = db.query(Role).filter(Role.id == role_id).first()
    if not get_role_id:
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": "Role Id does not exists"
            },
            status_code=400
        )
    '''
    role exist or not
    '''
    existing_role = db.query(Role).filter(Role.slug == role_data.slug).first()
    if existing_role:
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": "Role with this slug already exists"
            },
            status_code=400
        )
    '''
    Role Data Update
    '''
    get_role_id.slug = role_data.slug
    get_role_id.name = role_data.name

    # Commit the changes
    db.commit()
    db.refresh(get_role_id)
    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "Role has been update successfully!",
        },
        status_code=200
    )


'''
Delete role
role id does not exist
'''
@router.delete("/role/{role_id}/delete")
def delete_role_handler(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        return JSONResponse(
            content={
                "status": False,
                "code": 404,
                "message": "Role id does not exist!",
            },
            status_code=404
        )
    # Delete the role
    db.delete(db_role)
    db.commit()
    return JSONResponse(
        content={
            "status": True,
            "code": 200,
            "message": "Role has been deleted successfully!",
        },
        status_code=200
    )