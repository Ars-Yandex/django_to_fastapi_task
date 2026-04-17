import re
from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema

class CategoryBase(BaseSchema):
    title: str = Field(..., min_length=1, max_length=256)
    description: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    is_published: bool = True

    @field_validator('title', 'description', 'slug', mode='before')
    @classmethod
    def strip_and_check_empty(cls, v: str) -> str:
        """Очищает строку от пробелов и проверяет на пустоту"""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Поле не может быть пустым или состоять только из пробелов')
        return v

    @field_validator('slug')
    @classmethod
    def validate_slug_full(cls, v: str) -> str:
        """Проверка формата и краев слага"""
        if not re.match(r'^[-a-zA-Z0-9_]+$', v):
            raise ValueError(
                'В слаге могут использоваться только латинские буквы, цифры, дефис и нижнее подчеркивание'
            )
        
        if v.startswith(('-', '_')) or v.endswith(('-', '_')):
            raise ValueError('Слаг не может начинаться или заканчиваться дефисом или подчеркиванием')
            
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=256)
    description: Optional[str] = Field(None, min_length=1)
    slug: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None

    @field_validator('title', 'description', 'slug', mode='before')
    @classmethod
    def validate_optional_fields(cls, v: Optional[str]) -> Optional[str]:
        """При обновлении значение не должно быть пустым"""
        if v is not None and isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Переданное поле не может быть пустым')
            return v
        return v
    
    @field_validator('slug')
    @classmethod
    def validate_optional_slug_format(cls, v: Optional[str]) -> Optional[str]:
        """Проверка формата слага для обновлений"""
        if v:
            if not re.match(r'^[-a-zA-Z0-9_]+$', v):
                raise ValueError(
                    'В слаге могут использоваться только латинские буквы, цифры, дефис и нижнее подчеркивание'
                )
        return v

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True