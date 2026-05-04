from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class CommentModel(Base):
    __tablename__ = "blog_comment"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_published = Column(Boolean, default=True)
    
    post_id = Column(
        Integer, 
        ForeignKey("blog_post.id", ondelete="CASCADE"), 
        nullable=False
    )
    author_id = Column(
        Integer, 
        ForeignKey("auth_user.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    post = relationship("PostModel", back_populates="comments")
    author = relationship("UserModel", back_populates="comments")