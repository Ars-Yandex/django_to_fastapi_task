from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.posts import Post, PostCreate, PostUpdate
from src.database import get_db
from src.repositories.post import PostRepository

router = APIRouter()

@router.get("/posts", response_model=List[Post])
async def get_posts(db: AsyncSession = Depends(get_db)):
    """GET: Получение списка всех постов через репозиторий."""
    repository = PostRepository(db)
    return await repository.get_all()

@router.get("/posts/{id}", response_model=Post)
async def get_post_by_id(id: int, db: AsyncSession = Depends(get_db)):
    """GET: Получение одного поста по ID."""
    repository = PostRepository(db)
    post = await repository.get_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(post_in: PostCreate, db: AsyncSession = Depends(get_db)):
    """POST: Создание нового поста."""
    repository = PostRepository(db)
    return await repository.create(post_in.model_dump(), author_id=1)

@router.patch("/posts/{id}", response_model=Post)
async def update_post(id: int, post_in: PostUpdate, db: AsyncSession = Depends(get_db)):
    """PATCH: Частичное обновление поста."""
    repository = PostRepository(db)
    updated_post = await repository.update(id, post_in.model_dump(exclude_unset=True))
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_db)):
    """DELETE: Удаление поста."""
    repository = PostRepository(db)
    post = await repository.get_by_id(id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await repository.delete(id)
    return None