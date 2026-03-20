from fastapi import HTTPException
from src.repositories.user import UserRepository
from src.schemas.users import UserUpdate

class UpdateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int, update_data: UserUpdate):
        exists = await self.repo.get_by_id(user_id)
        if not exists:
            raise HTTPException(status_code=404, detail="User not found")
            
        data = update_data.model_dump(exclude_unset=True)
        return await self.repo.update(user_id, data)