from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.schemas.users import User

class Post(BaseModel):
    title: str = Field(..., max_length=256)
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)
    is_published: bool = True
    author: User

    class Config:
        from_attributes = True