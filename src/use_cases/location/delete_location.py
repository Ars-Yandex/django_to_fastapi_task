from fastapi import HTTPException
from src.repositories.location import LocationRepository

class DeleteLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_id: int):
        exists = await self.repo.get_by_id(loc_id)
        if not exists:
            raise HTTPException(status_code=404, detail="Location not found")
            
        await self.repo.delete(loc_id)
        return {"detail": "Location deleted successfully"}