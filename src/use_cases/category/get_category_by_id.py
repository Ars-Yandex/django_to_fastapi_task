from src.repositories.category import CategoryRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import CategoryNotFoundError

class GetCategoryByIdUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_id: int):
        try:
            return await self.repo.get_by_id(cat_id)
        except RecordNotFound:
            raise CategoryNotFoundError(cat_id)