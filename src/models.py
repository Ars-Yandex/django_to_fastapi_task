from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "auth_user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(254))
    password = Column(String(128))
    is_active = Column(Boolean, default=True)

class CategoryModel(Base):
    __tablename__ = "blog_category" 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    description = Column(Text)
    slug = Column(String, unique=True, index=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LocationModel(Base):
    __tablename__ = "blog_location" 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PostModel(Base):
    __tablename__ = "blog_post" 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    text = Column(Text)
    pub_date = Column(DateTime)
    is_published = Column(Boolean, default=True)
    image = Column(String, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    author_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False) 
    location_id = Column(Integer, ForeignKey("blog_location.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("blog_category.id"), nullable=True)

    author = relationship("UserModel")
    location = relationship("LocationModel")
    category = relationship("CategoryModel")