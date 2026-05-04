from src.repositories.user import UserRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import UserNotFoundError, ForbiddenError

class DeleteUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int, current_user):
        if not current_user.is_superuser and current_user.id != user_id:
            raise ForbiddenError("Вы не можете удалить чужой аккаунт")

        try:
            await self.repo.delete(user_id)
            return {"detail": f"Пользователь с ID {user_id} успешно удален"}
        except RecordNotFound:
            raise UserNotFoundError(user_id)