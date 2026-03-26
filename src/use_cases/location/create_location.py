from fastapi import HTTPException, status
from src.repositories.location import LocationRepository
from src.schemas.location import LocationCreate

class CreateLocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self, loc_data: LocationCreate):
        existing_loc = await self.repo.get_by_name(loc_data.name)
        if existing_loc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Location with name '{loc_data.name}' already exists"
            )

        return await self.repo.create(loc_data.model_dump())