from fastapi import HTTPException
from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryUpdate

class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_id: int, update_data: CategoryUpdate):
        exists = await self.repo.get_by_id(cat_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Category not found")
            
        return await self.repo.update(cat_id, update_data.model_dump())