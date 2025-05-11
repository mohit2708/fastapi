from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from database.connection import Base

class UserDetails(Base):
    __tablename__ = "user_details"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # Foreign key to User table
    user        = relationship("User", back_populates="user_details")  # Define relationship with User model

    address     = Column(String(255), nullable=True)
    state       = Column(String(255), nullable=True)
    city        = Column(String(255), nullable=True)
    zip_code    = Column(String(255), nullable=True)
    created_at  = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationship with User
    # user = relationship("User ", back_populates="user_details")
