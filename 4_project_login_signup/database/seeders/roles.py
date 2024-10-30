from database.models.roles import Role

def seed_roles(db):
    # Delete existing records
    db.query(Role).delete()
    db.commit()

    # Insert new data
    roles = [
        {"id": 1, "slug": "super_admin", "name": "Super Admin"},
        {"id": 2, "slug": "admin", "name": "Admin"},
        {"id": 3, "slug": "customer", "name": "Customer"},
        {"id": 4, "slug": "staff", "name": "Staff"},
        {"id": 5, "slug": "sample", "name": "Sample"},
        # Add more roles as needed
    ]
    for role_data in roles:
        role = Role(**role_data)
        db.add(role)
    db.commit()