from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))  # Define foreign key relationship
    role = relationship("Role", back_populates="users")  # Define relationship with Role model
    first_name = Column(String(255), nullable = True)
    last_name = Column(String(255))
    user_name = Column(String(255), unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255))
    zip_code = Column(String(255))
    is_active = Column(Boolean(), default=True)
    address = Column(String(255))
    country = Column(Integer)
    state = Column(Integer)
    city = Column(Integer)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)