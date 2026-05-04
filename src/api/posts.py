from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.posts import Post, PostCreate, PostUpdate
from src.schemas.users import User as UserSchema
from src.database import get_db
from src.api.dependencies import get_current_user

from src.repositories.post import PostRepository
from src.repositories.category import CategoryRepository
from src.repositories.location import LocationRepository
from src.repositories.user import UserRepository

from src.use_cases.post.get_all_posts import GetAllPostsUseCase
from src.use_cases.post.get_post_by_id import GetPostByIdUseCase
from src.use_cases.post.create_post import CreatePostUseCase
from src.use_cases.post.update_post import UpdatePostUseCase
from src.use_cases.post.delete_post import DeletePostUseCase

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[Post], summary="Get Posts")
async def get_posts(db: AsyncSession = Depends(get_db)):
    repository = PostRepository(db)
    return await GetAllPostsUseCase(repository).execute()

@router.get("/{id}", response_model=Post, summary="Get Post By Id")
async def get_post_by_id(id: int, db: AsyncSession = Depends(get_db)):
    repository = PostRepository(db)
    return await GetPostByIdUseCase(repository).execute(id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post, summary="Create Post")
async def create_post(
    post_in: PostCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    repository = PostRepository(db)
    cat_repo = CategoryRepository(db)
    loc_repo = LocationRepository(db)
    user_repo = UserRepository(db)
    
    use_case = CreatePostUseCase(
        repo=repository, 
        cat_repo=cat_repo, 
        loc_repo=loc_repo, 
        user_repo=user_repo
    )
    
    post_data = post_in.model_dump()
    post_data["author_id"] = current_user.id
    
    return await use_case.execute(post_data)

@router.patch("/{id}", response_model=Post, summary="Update Post")
async def update_post(
    id: int, 
    post_in: PostUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    repository = PostRepository(db)
    cat_repo = CategoryRepository(db)
    loc_repo = LocationRepository(db)
    
    use_case = UpdatePostUseCase(
        repo=repository, 
        cat_repo=cat_repo, 
        loc_repo=loc_repo
    )
    
    return await use_case.execute(id, post_in, current_user=current_user)

@router.delete("/{id}", status_code=status.HTTP_200_OK, summary="Delete Post")
async def delete_post(
    id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    repository = PostRepository(db)
    use_case = DeletePostUseCase(repository)
    
    return await use_case.execute(id, current_user=current_user)