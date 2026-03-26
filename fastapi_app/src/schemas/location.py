from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema

class LocationBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=256)
    is_published: bool = True

    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Название локации не может быть пустым или состоять только из пробелов')
        return v

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=256)
    is_published: Optional[bool] = None

class Location(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True