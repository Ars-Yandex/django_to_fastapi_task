from fastapi import HTTPException
from src.repositories.post import PostRepository

class DeletePostUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: int):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
            
        await self.repo.delete(post_id)
        return {"detail": "Post deleted successfully"}