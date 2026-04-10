from src.repositories.post import PostRepository
from src.repositories.category import CategoryRepository
from src.repositories.location import LocationRepository
from src.schemas.posts import PostUpdate
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import (
    PostNotFoundError, 
    CategoryNotFoundError, 
    LocationNotFoundError
)

class UpdatePostUseCase:
    def __init__(self, repo: PostRepository, cat_repo: CategoryRepository, loc_repo: LocationRepository):
        self.repo = repo
        self.cat_repo = cat_repo
        self.loc_repo = loc_repo

    async def execute(self, post_id: int, update_data: PostUpdate):
        data = update_data.model_dump(exclude_unset=True)
        try:
            if data.get("category_id"):
                await self.cat_repo.get_by_id(data["category_id"])
            
            if data.get("location_id"):
                await self.loc_repo.get_by_id(data["location_id"])
            
            return await self.repo.update(post_id, data)
            
        except RecordNotFound as e:
            if e.model == "Post": 
                raise PostNotFoundError(post_id)
                
            if e.model == "Category": 
                raise CategoryNotFoundError(data["category_id"])
                
            if e.model == "Location": 
                raise LocationNotFoundError(data["location_id"])
                
            raise