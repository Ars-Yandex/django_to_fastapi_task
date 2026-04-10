from src.repositories.location import LocationRepository
from src.schemas.location import LocationUpdate
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import (
    LocationNotFoundError, 
    LocationAlreadyExistsError
)

class UpdateLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_id: int, update_data: LocationUpdate):
        current_loc = await self.repo.get_by_id(loc_id)
        if not current_loc:
            raise LocationNotFoundError(loc_id)

        if update_data.name:
            existing_loc = await self.repo.get_by_name(update_data.name)
            if existing_loc and existing_loc.id != loc_id:
                raise LocationAlreadyExistsError(name=update_data.name)

        try:
            data = update_data.model_dump(exclude_unset=True)
            return await self.repo.update(loc_id, data)
        except RecordNotFound:
            raise LocationNotFoundError(loc_id)