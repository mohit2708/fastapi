from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, ORJSONResponse
from sqlalchemy.orm import Session
from database.models.role import Role
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError



from database.connection import get_db

# from database.repository.role import get_roles

from database.schemas.role import RoleList, RoleDetail, RoleCreate, RoleUpdate, RoleDelete

from typing import List

router = APIRouter()


'''
Get role List
'''
@router.get("/role-list/", response_model=List[RoleList])
def get_roles_list(db: Session = Depends(get_db)):
    roles = get_roles(db)
    # return roles
    role_data = {
        "success": True,
        "code": 200,
        "message":"hello",
        "roles": roles
    }
    response_data= RoleList(**role_data)
    return ORJSONResponse(content=response_data.dict(), status_code=200)

def get_roles(db: Session) -> List[dict]:
    roles = db.query(Role.id, Role.slug, Role.name).all()
    roles_list = []
    for role in roles:
        role_dict = {
            "id": role.id,
            "slug": role.slug,
            "name": role.name
        }
        roles_list.append(role_dict)
    return roles_list


'''
Get role List by id
'''
@router.get("/role/{role_id}", response_model=RoleDetail)
def get_role_by_id(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    # if not role:
    if role is None:
        # raise HTTPException(status_code=404, detail="Role not found")
        return ORJSONResponse(
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
Create role
validation exsting role
role id does not exist
'''
@router.post("/role/create")
def create_role_handler(role: RoleCreate, db: Session = Depends(get_db)):
    # Check Existing Role
    try:
        existing_role = db.query(Role).filter(Role.slug == role.slug).first()
        if existing_role:
            return ORJSONResponse(
                content={
                    "status": False,
                    "code": 400,
                    "message": "Role with this slug already exists"
                },
                status_code=400
            )
        
        # Save role
        # db_role = create_role(role=role, db=db)
        db_role = Role(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        if isinstance(db_role, Role):
            return JSONResponse(
                content={
                    "status": True,
                    "code": 200,
                    "message": "Role has been created successfully!",
                    "data": {
                        "id": db_role.id,
                        "slug": db_role.slug,
                        "name": db_role.name,
                        "created_at": db_role.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                        "updated_at": db_role.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
                    }
                },
                status_code=200
            )
        else:
            return db_role  # Return the existing response if the role already exists
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



'''
Update role
validation exsting role
role id does not exist
'''
@router.put("/role/{role_id}/update", response_model=RoleUpdate)
def update_role_handler(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):
    existing_role = db.query(Role).filter(Role.slug == role_data.slug).first()
    if existing_role:
        return JSONResponse(
            content={
                "status": False,
                "code": 400,
                "message": "Role with the same slug already exists!",
            },
            status_code=400
        )
    updated_role = update_role(db, role_id, role_data)
    if isinstance(updated_role, Role):
        return JSONResponse(
                    content={
                        "status": True,
                        "code": 200,
                        "message": "Role has been update successfully!",
                        "data": {
                            "id": updated_role.id,
                            "slug": updated_role.slug,
                            "name": updated_role.name,
                            "created_at": updated_role.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
                            "updated_at": updated_role.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
                        }
                    },
                    status_code=200
                )
    if updated_role is None:
        return JSONResponse(
                content={
                    "status": False,
                    "code": 404,
                    "message": "Role id does not exist!",
                },
                status_code=404
            )
    return updated_role

def update_role(db: Session, role_id: int, role_data: RoleUpdate):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        for key, value in role_data.dict().items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
        return db_role
    return None


'''
Delete role
role id does not exist
'''
@router.delete("/role/{role_id}/delete", response_model=RoleDelete)
def delete_role_handler(role_id: int, db: Session = Depends(get_db)):
    deleted_role = delete_role(db, role_id)
    if not deleted_role:
        return JSONResponse(
                content={
                    "status": False,
                    "code": 404,
                    "message": "Role id does not exist!",
                },
                status_code=404
            )
    return deleted_role

def delete_role(db: Session, role_id: int) -> RoleDelete:
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if db_role:
        deleted_role = RoleDelete(**db_role.__dict__)
        db.delete(db_role)
        db.commit()
        return JSONResponse(
            content={
                "status": True,
                "code": 200,
                "message": "Role has been Delete successfully!",
            },
            status_code=200
        )
        # return deleted_role
    return None

# ================================================================================ router


# @router.put("/role/{role_id}/update", response_model=RoleUpdate)
# def update_role_handler(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):
#     # updated_role = update_role(db, role_id, role_data)
#     db_role = db.query(Role).filter(Role.id == role_id).first()
#     if db_role:
#         for key, value in role_data.dict().items():
#             setattr(db_role, key, value)
#         db.commit()
#         db.refresh(db_role)

#         # return db_role
#         db_role_dict = {
#             "id": db_role.id,
#             "slug": db_role.slug,
#             "name": db_role.name,
#             # Add other attributes as needed
#         }
        
#         response_data = {
#             "success": True,
#             "message": "Role updated successfully",
#             "data": db_role_dict,
#             # "data": db_role.dict(),  # Convert db_role to dictionary # not working this line
#             "status": 200
#         }
#         return JSONResponse(content=response_data, status_code=200)

#     if db_role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     return db_role




# @router.put("/role/{role_id}/update", response_model=RoleUpdate)
# def update_role_handler(role_id: int, role_data: RoleUpdate, db: Session = Depends(get_db)):
#     db_role = db.query(Role).filter(Role.id == role_id).first()
#     if db_role:
#         if role_data.slug:  # If slug is provided in the request
#             db_role.slug = role_data.slug
#         for key, value in role_data.dict().items():
#             # Skip updating slug as it's already updated if provided
#             if key != 'slug':
#                 setattr(db_role, key, value)
#         db.commit()
#         db.refresh(db_role)
        
#         # Construct dictionary from Role object
#         db_role_dict = {
#             "id": db_role.id,
#             "name": db_role.name,
#             "slug": db_role.slug if hasattr(db_role, 'slug') else None,
#             # Add other attributes as needed
#         }
        
#         response_data = {
#             "success": True,
#             "message": "Role updated successfully",
#             "data": db_role_dict,
#             "status": 200
#         }
#         return JSONResponse(content=response_data, status_code=200)

#     raise HTTPException(status_code=404, detail="Role not found")



#### =================================================================================================
##   json return

# 1st 

# return JSONResponse(
#     content={
#         "status": True,
#         "code": 200,
#         "message": "Role has been Delete successfully!",
#     },
#     status_code=200
# )

# 2nd
# return {
#             "status": True,
#             "code": 200,
#             "message": "Role has been created successfully!",
#             "data": {
#                 "id": db_role.id,
#                 "slug": db_role.slug,
#                 "name": db_role.name,
#                 "created_at": db_role.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
#                 "updated_at": db_role.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
#             }
#         }

# 2nd

# raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Role with this slug already exists",
#             headers={"X-Error": "There goes my error"},
#         )


# 3rd

