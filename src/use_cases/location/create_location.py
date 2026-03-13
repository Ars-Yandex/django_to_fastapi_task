from src.repositories.location import LocationRepository
from src.schemas.location import LocationCreate

class CreateLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_data: LocationCreate):
        return await self.repo.create(loc_data.model_dump())