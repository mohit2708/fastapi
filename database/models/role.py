from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database.connection import Base

class Role(Base):
    __tablename__ = "roles"

    id          = Column(Integer, primary_key=True, index=True)
    slug        = Column(String(255), nullable=True)
    name        = Column(String(255), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    users = relationship("User", back_populates="role")  # Define reverse relationship with User model


