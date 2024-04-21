from database.models.role import Role
from sqlalchemy.orm import Session

def seed_roles(db: Session):
    roles = [
        {"id": 1, "slug": "admin", "name": "Admin"},
        {"id": 2, "slug": "staff", "name": "Staff"},
        # Add more roles as needed
    ]
    for role_data in roles:
        role = Role(**role_data)
        db.merge(role)  # Perform upsert (insert or update)
    db.commit()



# from database.models.role import Role  # Import your Role model here if needed

# def seed_roles(db):
#     # Delete existing records
#     db.query(Role).delete()
#     db.commit()

#     # Insert new data
#     roles = [
#         {"id": 1, "name": "Admin"},
#         {"id": 2, "name": "User"},
#         # Add more roles as needed
#     ]
#     for role_data in roles:
#         role = Role(**role_data)
#         db.add(role)
#     db.commit()
