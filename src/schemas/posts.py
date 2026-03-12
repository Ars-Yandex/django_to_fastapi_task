from pydantic import Field
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema
from src.schemas.users import User
from src.schemas.location import Location
from src.schemas.category import Category

class PostBase(BaseSchema):
    title: str = Field(..., max_length=256)
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    is_published: bool = True
    image: Optional[str] = None

class PostCreate(PostBase):
    """Схема только для создания: принимаем ID связей."""
    location_id: Optional[int] = None
    category_id: Optional[int] = None

class PostUpdate(PostBase):
    """Схема для обновления: все поля необязательны."""
    title: Optional[str] = Field(None, max_length=256)
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None

class Post(PostBase):
    """Схема для ответа: возвращаем полные объекты."""
    id: int
    author: User
    location: Optional[Location] = None 
    category: Optional[Category] = None