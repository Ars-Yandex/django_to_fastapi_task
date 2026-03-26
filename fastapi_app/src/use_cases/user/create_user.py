from fastapi import HTTPException, status
from src.repositories.user import UserRepository
from src.schemas.users import UserCreate

class CreateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_data: UserCreate):
        if await self.repo.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with username '{user_data.username}' already exists"
            )
        
        if await self.repo.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email '{user_data.email}' already exists"
            )
        
        return await self.repo.create(user_data.model_dump())