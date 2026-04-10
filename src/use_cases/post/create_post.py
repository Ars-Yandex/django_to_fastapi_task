from src.repositories.post import PostRepository
from src.repositories.category import CategoryRepository
from src.repositories.location import LocationRepository
from src.repositories.user import UserRepository
from src.schemas.posts import PostCreate
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import (
    UserNotFoundError, 
    CategoryNotFoundError, 
    LocationNotFoundError
)

class CreatePostUseCase:
    def __init__(self, repo: PostRepository, cat_repo: CategoryRepository, 
                 loc_repo: LocationRepository, user_repo: UserRepository):
        self.repo = repo
        self.cat_repo = cat_repo
        self.loc_repo = loc_repo
        self.user_repo = user_repo

    async def execute(self, post_data: PostCreate):
        data = post_data.model_dump()
        author_id = data.pop("author_id")
        
        try:
            await self.user_repo.get_by_id(author_id)
            
            if data.get("category_id"):
                await self.cat_repo.get_by_id(data["category_id"])
                
            if data.get("location_id"):
                await self.loc_repo.get_by_id(data["location_id"])

            return await self.repo.create(data, author_id)
            
        except RecordNotFound as e:
            if e.model == "User": 
                raise UserNotFoundError(author_id)
            
            if e.model == "Category": 
                raise CategoryNotFoundError(data["category_id"])
            
            if e.model == "Location": 
                raise LocationNotFoundError(data["location_id"])
                
            raise