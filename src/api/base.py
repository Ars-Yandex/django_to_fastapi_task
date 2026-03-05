from fastapi import APIRouter, status, HTTPException
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from src.schemas.posts import Post
from typing import List

Base = declarative_base()

class CategoryModel(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    slug = Column(String, unique=True)
    is_published = Column(Boolean, default=True)

class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    text = Column(Text)
    is_published = Column(Boolean, default=True)

router = APIRouter()
fake_db = []

@router.get("/posts", response_model=List[Post])
async def get_posts():
    return fake_db

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post: Post):
    fake_db.append(post)
    return post

@router.put("/posts/{id}", response_model=Post)
async def update_post(id: int, updated_post: Post):
    if 0 <= id < len(fake_db):
        fake_db[id] = updated_post
        return updated_post
    raise HTTPException(status_code=404, detail="Not found")

@router.delete("/posts/{id}")
async def delete_post(id: int):
    if 0 <= id < len(fake_db):
        fake_db.pop(id)
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Not found")