from src.repositories.category import CategoryRepository

class GetAllCategoriesUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.get_all()