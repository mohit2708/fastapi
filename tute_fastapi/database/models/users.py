from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, Session
from database.connection import Base
from passlib.context import CryptContext

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)  # Define foreign key relationship
    role = relationship("Role", back_populates="users")  # Define relationship with Role model
    
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    user_name = Column(String(255), unique=True, index=True, nullable=True)
    email = Column(String(255), nullable=True, unique=True, index=True)
    password = Column(String(255), nullable=True)

    image = Column(String(255), nullable=True)  # Field for image upload
    
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user_details = relationship("UserDetails", back_populates="user", uselist=False, cascade="all, delete-orphan")

    # note: user_details relationship in User: uselist=False is used here since each user should have only one UserDetails record.


    # Define relationship with UserDetails
    # user_details = relationship("UserDetails", back_populates="users", cascade="all, delete-orphan")

    """
    check plain_password or hashed_password are same
    """
    # Verify password(Match password) 
    @staticmethod
    def verify_password(plain_password, hashed_password):
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return password_context.verify(plain_password, hashed_password)

    # 1 type get email
    # @classmethod
    # def get_email(cls, db: Session, request):
    #     return db.query(cls).filter(cls.email == request.email).first()

    # 2 type get email
    def get_user_by_email(db: Session, requestemail):
        return db.query(User).filter(User.email == requestemail).first()
    

    def get_user_by_username(db: Session, requestusername):
        return db.query(User).filter(User.user_name == requestusername).first()

    """
    check user exist or not
    """
    # def get_user_by_username(db: Session, request):
    #     return db.query(User).filter(User.user_name == request.username).first()