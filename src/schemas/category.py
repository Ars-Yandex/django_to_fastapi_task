from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema

class CategoryBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=256)
    description: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: bool = True

    @field_validator('title', 'description', 'slug')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Поле не может быть пустым или состоять только из пробелов')
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1, pattern=r'^[-a-zA-Z0-9_]+$')
    is_published: Optional[bool] = None

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True