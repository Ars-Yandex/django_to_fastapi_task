from src.repositories.post import PostRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import PostNotFoundError

class DeletePostUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: int):
        try:
            await self.repo.delete(post_id)
            return {"detail": f"Пост с ID {post_id} успешно удален"}
        except RecordNotFound:
            raise PostNotFoundError(post_id=post_id)