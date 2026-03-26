from fastapi import HTTPException
from src.repositories.location import LocationRepository
from src.schemas.location import LocationUpdate

class UpdateLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_id: int, update_data: LocationUpdate):
        exists = await self.repo.get_by_id(loc_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Location not found")
            
        data = update_data.model_dump(exclude_unset=True)
        return await self.repo.update(loc_id, data)