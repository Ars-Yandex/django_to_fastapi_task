from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database import get_db
from src.repositories.user import UserRepository
from src.schemas.users import User, UserCreate, UserUpdate

from src.use_cases.user.get_all_users import GetAllUsersUseCase
from src.use_cases.user.get_user_by_id import GetUserByIdUseCase
from src.use_cases.user.create_user import CreateUserUseCase
from src.use_cases.user.update_user import UpdateUserUseCase
from src.use_cases.user.delete_user import DeleteUserUseCase

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[User])
async def get_users(session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    return await GetAllUsersUseCase(repo).execute()

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    return await CreateUserUseCase(repo).execute(user_in)

@router.get("/{id}", response_model=User, summary="Get User By Id")
async def get_user(id: int, session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    return await GetUserByIdUseCase(repo).execute(id)

@router.patch("/{id}", response_model=User)
async def update_user(id: int, user_in: UserUpdate, session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    return await UpdateUserUseCase(repo).execute(id, user_in)

@router.delete("/{id}")
async def delete_user(id: int, session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    return await DeleteUserUseCase(repo).execute(id)