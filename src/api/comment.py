from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_db
from src.repositories.comment import CommentRepository
from src.repositories.post import PostRepository
from src.repositories.user import UserRepository
from src.schemas.comments import Comment, CommentCreate, CommentUpdate

from src.use_cases.comment.create_comment import CreateCommentUseCase
from src.use_cases.comment.get_all_comments import GetAllCommentsUseCase
from src.use_cases.comment.get_comment_by_id import GetCommentByIdUseCase
from src.use_cases.comment.update_comment import UpdateCommentUseCase
from src.use_cases.comment.delete_comment import DeleteCommentUseCase

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.get("/", response_model=List[Comment])
async def get_comments(session: AsyncSession = Depends(get_db)):
    repo = CommentRepository(session)
    return await GetAllCommentsUseCase(repo).execute()

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(comm_in: CommentCreate, session: AsyncSession = Depends(get_db)):
    repo = CommentRepository(session)
    post_repo = PostRepository(session)
    user_repo = UserRepository(session)
    
    use_case = CreateCommentUseCase(
        repo=repo, 
        post_repo=post_repo, 
        user_repo=user_repo
    )
    return await use_case.execute(comm_in)

@router.get("/{id}", response_model=Comment)
async def get_comment(id: int, session: AsyncSession = Depends(get_db)):
    repo = CommentRepository(session)
    return await GetCommentByIdUseCase(repo).execute(id)

@router.patch("/{id}", response_model=Comment)
async def update_comment(id: int, comm_in: CommentUpdate, session: AsyncSession = Depends(get_db)):
    repo = CommentRepository(session)
    return await UpdateCommentUseCase(repo).execute(id, comm_in)

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_comment(id: int, session: AsyncSession = Depends(get_db)):
    repo = CommentRepository(session)
    result = await DeleteCommentUseCase(repo).execute(id)
    return result