from src.repositories.user import UserRepository
from src.schemas.users import UserCreate

class CreateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_data: UserCreate):
        return await self.repo.create(user_data.model_dump())