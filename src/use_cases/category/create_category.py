from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryCreate

class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_data: CategoryCreate):
        return await self.repo.create(cat_data.model_dump())