from pydantic import EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from src.schemas.base import BaseSchema

class UserBase(BaseSchema):
    username: str = Field(..., min_length=1, max_length=150)
    email: EmailStr = Field(..., max_length=254)
    is_active: bool = True

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if v is not None:
            if ' ' in v:
                raise ValueError('Имя пользователя не может содержать пробелы')
            if not v.strip():
                raise ValueError('Имя пользователя не может быть пустым')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = Field(None, max_length=254)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8, max_length=128)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if ' ' in v:
                raise ValueError('Имя пользователя не может содержать пробелы')
            if not v.strip():
                raise ValueError('Имя пользователя не может быть пустым')
        return v

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)