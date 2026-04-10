from src.repositories.location import LocationRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import LocationNotFoundError

class DeleteLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_id: int):
        try:
            await self.repo.delete(loc_id)
            return {"detail": f"Локация с ID {loc_id} успешно удалена"}
        except RecordNotFound:
            raise LocationNotFoundError(loc_id)