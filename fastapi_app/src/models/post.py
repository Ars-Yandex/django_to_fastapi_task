from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

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