from fastapi import HTTPException, status
from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryCreate

class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_data: CategoryCreate):
        existing_cat = await self.repo.get_by_slug(cat_data.slug)
        if existing_cat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with slug '{cat_data.slug}' already exists"
            )
            
        return await self.repo.create(cat_data.model_dump())