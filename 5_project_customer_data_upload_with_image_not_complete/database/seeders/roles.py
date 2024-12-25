from database.models.roles import Role

def seed_roles(db):
    # Retrieve all existing slugs from the database
    existing_slugs = {role.slug for role in db.query(Role).all()}
    
    # Define roles to insert
    roles = [
        {"id": 1, "slug": "super_admin", "name": "Super Admin"},
        {"id": 2, "slug": "admin", "name": "Admin"},
        {"id": 3, "slug": "customer", "name": "Customer"},
        {"id": 4, "slug": "staff", "name": "Staff"},
        {"id": 5, "slug": "sample", "name": "Sample"},
    ]
    
    # Filter roles to only those not already in the database
    roles_to_insert = [role_data for role_data in roles if role_data["slug"] not in existing_slugs]

    if roles_to_insert:
        for role_data in roles_to_insert:
            role = Role(**role_data)
            db.add(role)
        db.commit()
        print("New roles seeded successfully.")
    else:
        print("Roles already seeded, no new roles to add.")

