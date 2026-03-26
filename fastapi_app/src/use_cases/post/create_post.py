from fastapi import HTTPException
from src.repositories.post import PostRepository
from src.repositories.category import CategoryRepository
from src.repositories.location import LocationRepository
from src.repositories.user import UserRepository
from src.schemas.posts import PostCreate

class CreatePostUseCase:
    def __init__(
        self, 
        repo: PostRepository, 
        cat_repo: CategoryRepository, 
        loc_repo: LocationRepository,
        user_repo: UserRepository
    ):
        self.repo = repo
        self.cat_repo = cat_repo
        self.loc_repo = loc_repo
        self.user_repo = user_repo

    async def execute(self, post_data: PostCreate):
        data = post_data.model_dump()
        
        author = await self.user_repo.get_by_id(data["author_id"])
        if not author:
            raise HTTPException(status_code=422, detail=f"User {data['author_id']} not exists")

        if data.get("category_id"):
            category = await self.cat_repo.get_by_id(data["category_id"])
            if not category:
                raise HTTPException(status_code=422, detail=f"Category {data['category_id']} not exists")
        
        if data.get("location_id"):
            location = await self.loc_repo.get_by_id(data["location_id"])
            if not location:
                raise HTTPException(status_code=422, detail=f"Location {data['location_id']} not exists")

        author_id = data.pop("author_id")
        return await self.repo.create(data, author_id)