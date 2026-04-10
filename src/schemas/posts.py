from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.schemas.users import User
from src.schemas.location import Location
from src.schemas.category import Category

class PostBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=256)
    text: str = Field(..., min_length=1)
    pub_date: datetime = Field(default_factory=datetime.now)
    is_published: bool = True
    image: Optional[str] = None

    @field_validator('title', 'text', mode='before')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Поле не может быть пустым или состоять только из пробелов')
        return v

class PostCreate(PostBase):
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None

class PostUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    text: Optional[str] = Field(None, min_length=1)
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    image: Optional[str] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None

    @field_validator('title', 'text', mode='before')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Поле не может быть пустым')
        return v

class Post(PostBase):
    id: int
    author: User
    location: Optional[Location] = None 
    category: Optional[Category] = None

    class Config:
        from_attributes = True