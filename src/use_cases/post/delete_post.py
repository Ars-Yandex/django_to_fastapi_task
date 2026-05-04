from src.repositories.post import PostRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import PostNotFoundError, ForbiddenError

class DeletePostUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: int, current_user):
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)

        if not current_user.is_superuser and post.author_id != current_user.id:
            raise ForbiddenError("У вас нет прав для удаления этого поста")

        try:
            await self.repo.delete(post_id)
            return {"detail": f"Пост {post_id} успешно удален"}
        except RecordNotFound:
            raise PostNotFoundError(post_id)