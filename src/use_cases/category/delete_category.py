from src.repositories.category import CategoryRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import CategoryNotFoundError

class DeleteCategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def execute(self, cat_id: int):
        try:
            await self.repo.delete(cat_id)
            return {"detail": f"Категория с ID {cat_id} успешно удалена"}
        except RecordNotFound:
            raise CategoryNotFoundError(cat_id)