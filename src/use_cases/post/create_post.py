from src.repositories.post import PostRepository
from src.schemas.posts import PostCreate

class CreatePostUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_data: PostCreate, author_id: int):
        return await self.repo.create(post_data.model_dump(), author_id)