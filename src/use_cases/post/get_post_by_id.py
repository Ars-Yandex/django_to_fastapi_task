from src.repositories.post import PostRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import PostNotFoundError

class GetPostByIdUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: int):
        try:
            return await self.repo.get_by_id(post_id)
        except RecordNotFound:
            raise PostNotFoundError(post_id=post_id)