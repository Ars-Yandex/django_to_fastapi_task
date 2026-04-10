import re
from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema

class LocationBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=256)
    is_published: bool = True

    @field_validator('name', mode='before')
    @classmethod
    def strip_name(cls, v: str) -> str:
        """Предварительная очистка от пробелов"""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Название локации не может быть пустым')
        return v

    @field_validator('name')
    @classmethod
    def validate_name_content(cls, v: str) -> str:
        """Разрешаем буквы (рус/англ), цифры и дефис"""
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s-]+$', v):
            raise ValueError(
                'Название может содержать только буквы (русские/латинские), цифры, пробелы и дефис'
            )
        
        if v.startswith(('-', '_')) or v.endswith(('-', '_')):
            raise ValueError('Название не может начинаться или заканчиваться дефисом или подчеркиванием')
            
        return v

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=256)
    is_published: Optional[bool] = None

    @field_validator('name', mode='before')
    @classmethod
    def validate_optional_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Название не может быть пустым')
            
            if not re.match(r'^[a-zA-Zа-яА-Я0-9\s-]+$', v):
                raise ValueError('Недопустимые символы в названии')
            if v.startswith(('-', '_')) or v.endswith(('-', '_')):
                raise ValueError('Название не может начинаться или заканчиваться спецсимволом')
        return v

class Location(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True