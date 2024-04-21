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



# from database.models.base_class import Base
# from sqlalchemy import Boolean, Column, Integer, String, DateTime
# from datetime import datetime
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship


# class User(Base):
#     id = Column(Integer, primary_key=True, index=True)
#     # role_id = Column(Integer, nullable=True)
#     role_id = Column(Integer, ForeignKey('role.id'), nullable=True)  # ForeignKey relationship
#     first_name = Column(String(255), nullable = True)
#     last_name = Column(String(255), index=True, nullable = True)
#     email = Column(String(255), nullable=False, unique=True, index=True)
#     password = Column(String(255), nullable=False)
#     # is_superuser = Column(Boolean(), default=False)
#     is_active = Column(Boolean(), default=True)
#     # blogs = relationship("Blog",back_populates="author")
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     role = relationship("Role", back_populates="users")  # Define the relationship


