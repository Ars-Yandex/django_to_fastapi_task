from fastapi import HTTPException
from src.repositories.user import UserRepository

class DeleteUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int):
        exists = await self.repo.get_by_id(user_id)
        if not exists:
            raise HTTPException(status_code=404, detail="User not found")
            
        await self.repo.delete(user_id)
        return {"detail": "User deleted successfully"}