from fastapi import HTTPException
from src.repositories.post import PostRepository
from src.schemas.posts import PostUpdate

class UpdatePostUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: int, update_data: PostUpdate):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
            
        data = update_data.model_dump(exclude_unset=True)
        return await self.repo.update(post_id, data)