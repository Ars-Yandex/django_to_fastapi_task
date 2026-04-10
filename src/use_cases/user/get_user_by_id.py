from src.repositories.user import UserRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import UserNotFoundError

class GetUserByIdUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int):
        try:
            return await self.repo.get_by_id(user_id)
        except RecordNotFound:
            raise UserNotFoundError(user_id)