from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class UserModel(Base):
    __tablename__ = "auth_user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(254))
    password = Column(String(128))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    first_name = Column(String(150), default="")
    last_name = Column(String(150), default="")

    posts = relationship(
        "PostModel", 
        back_populates="author", 
        cascade="all, delete-orphan"
    )
    
    comments = relationship(
        "CommentModel", 
        back_populates="author", 
        cascade="all, delete-orphan"
    )