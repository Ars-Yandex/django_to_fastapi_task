from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryCreate
from src.exceptions.database_exceptions import AlreadyExists
from src.exceptions.domain_exceptions import CategoryAlreadyExistsError

class CreateCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_data: CategoryCreate):
        try:
            return await self.repo.create(cat_data.model_dump())
        except AlreadyExists:
            raise CategoryAlreadyExistsError(cat_data.slug)