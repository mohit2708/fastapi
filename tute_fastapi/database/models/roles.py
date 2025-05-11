from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database.connection import Base

# Role Table
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(255), nullable=False, unique=True)  # unique slug for each role
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    users = relationship("User", back_populates="role", cascade="all, delete-orphan")