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

    @field_validator('title', 'text')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if isinstance(v, str) and not v.strip():
            raise ValueError('Поле не может быть пустым или состоять только из пробелов')
        return v

class PostCreate(PostBase):
    """Схема для создания: принимаем ID автора и связей."""
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None

class PostUpdate(BaseSchema):
    """Схема для обновления: все поля необязательны."""
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    text: Optional[str] = Field(None, min_length=1)
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    image: Optional[str] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None

class Post(PostBase):
    """Схема для ответа: возвращаем полные объекты."""
    id: int
    author: User
    location: Optional[Location] = None 
    category: Optional[Category] = None

    class Config:
        from_attributes = True