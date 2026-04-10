from src.repositories.location import LocationRepository
from src.schemas.location import LocationCreate
from src.exceptions.domain_exceptions import LocationAlreadyExistsError

class CreateLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_data: LocationCreate):
        existing_loc = await self.repo.get_by_name(loc_data.name)
        if existing_loc:
            raise LocationAlreadyExistsError(name=loc_data.name)

        return await self.repo.create(loc_data.model_dump())