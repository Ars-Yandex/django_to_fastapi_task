from fastapi import HTTPException
from src.repositories.post import PostRepository
from src.repositories.category import CategoryRepository
from src.repositories.location import LocationRepository
from src.schemas.posts import PostUpdate

class UpdatePostUseCase:
    def __init__(self, repo: PostRepository, cat_repo: CategoryRepository, loc_repo: LocationRepository):
        self.repo = repo
        self.cat_repo = cat_repo
        self.loc_repo = loc_repo

    async def execute(self, post_id: int, update_data: PostUpdate):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
            
        data = update_data.model_dump(exclude_unset=True)

        if "category_id" in data and data["category_id"] is not None:
            category = await self.cat_repo.get_by_id(data["category_id"])
            if not category:
                raise HTTPException(status_code=422, detail=f"Category {data['category_id']} not found")

        if "location_id" in data and data["location_id"] is not None:
            location = await self.loc_repo.get_by_id(data["location_id"])
            if not location:
                raise HTTPException(status_code=422, detail=f"Location {data['location_id']} not found")

        return await self.repo.update(post_id, data)