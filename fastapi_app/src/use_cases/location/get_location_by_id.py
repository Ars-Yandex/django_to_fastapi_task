from fastapi import HTTPException
from src.repositories.location import LocationRepository

class GetLocationByIdUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_id: int):
        location = await self.repo.get_by_id(loc_id)
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        return location