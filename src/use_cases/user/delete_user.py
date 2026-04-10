from src.repositories.user import UserRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import UserNotFoundError

class DeleteUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int):
        try:
            await self.repo.delete(user_id)
            return {"detail": f"Пользователь с ID {user_id} успешно удален"}
            
        except RecordNotFound:
            raise UserNotFoundError(user_id)