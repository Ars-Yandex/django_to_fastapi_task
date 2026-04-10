from src.repositories.location import LocationRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import LocationNotFoundError

class GetLocationByIdUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_id: int):
        try:
            return await self.repo.get_by_id(loc_id)
        except RecordNotFound:
            raise LocationNotFoundError(loc_id)