from pydantic import EmailStr, Field, field_validator
from typing import Optional
from src.schemas.base import BaseSchema

class UserBase(BaseSchema):
    username: str = Field(..., min_length=1, max_length=150)
    email: Optional[str] = Field(None, max_length=254)
    is_active: bool = True

    @field_validator('username')
    @classmethod
    def username_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Имя пользователя не может быть пустым или состоять только из пробелов')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

class User(UserBase):
    id: int