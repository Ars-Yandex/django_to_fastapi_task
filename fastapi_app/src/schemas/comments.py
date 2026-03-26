from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.schemas.users import User

class CommentBase(BaseSchema):
    text: str = Field(..., min_length=1, description="Текст комментария")
    is_published: bool = True

    @field_validator('text')
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Комментарий не может быть пустым или состоять только из пробелов')
        return v

class CommentCreate(CommentBase):
    author_id: int
    post_id: int

class CommentUpdate(BaseSchema):
    text: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None

class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True