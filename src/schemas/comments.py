import re
from pydantic import Field, field_validator
from datetime import datetime
from typing import Optional
from src.schemas.base import BaseSchema

class CommentBase(BaseSchema):
    text: str = Field(..., min_length=1, description="Текст комментария")
    is_published: bool = True

    @field_validator('text', mode='before')
    @classmethod
    def strip_text(cls, v: str) -> str:
        """Удаляем лишние пробелы по краям и проверяем на пустоту"""
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError('Комментарий не может быть пустым')
        return v

    @field_validator('text')
    @classmethod
    def validate_text_content(cls, v: str) -> str:
        """Проверка на допустимые символы (буквы, цифры, пунктуация)"""
        if not re.match(r'^[a-zA-Zа-яА-Я0-9\s.,!?\-:;()"\']+$', v):
            raise ValueError(
                'Текст содержит недопустимые спецсимволы (разрешены буквы, цифры и знаки препинания)'
            )
        return v

class CommentCreate(CommentBase):
    author_id: int
    post_id: int

class CommentUpdate(BaseSchema):
    text: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None

    @field_validator('text', mode='before')
    @classmethod
    def validate_optional_text(cls, v: Optional[str]) -> Optional[str]:
        """Для обновлений: если текст пришел, он не должен быть пустым"""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Текст комментария не может быть пустым')
        return v

class Comment(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True