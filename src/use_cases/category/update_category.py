from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryUpdate
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import (
    CategoryNotFoundError, 
    CategoryAlreadyExistsError
)

class UpdateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_id: int, update_data: CategoryUpdate):
        data = update_data.model_dump(exclude_unset=True)
        
        if "slug" in data:
            existing_category = await self.repo.get_by_slug(data["slug"])
            
            if existing_category and existing_category.id != cat_id:
                raise CategoryAlreadyExistsError(data["slug"])

        try:
            return await self.repo.update(cat_id, data)
        except RecordNotFound:
            raise CategoryNotFoundError(cat_id)