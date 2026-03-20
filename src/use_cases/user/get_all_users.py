from src.repositories.user import UserRepository

class GetAllUsersUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.get_all()