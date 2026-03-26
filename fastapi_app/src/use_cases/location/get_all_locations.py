from src.repositories.location import LocationRepository

class GetAllLocationsUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.get_all()