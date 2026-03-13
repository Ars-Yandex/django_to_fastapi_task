from src.repositories.post import PostRepository

class GetAllPostsUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.get_all()