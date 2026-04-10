from src.repositories.comment import CommentRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import CommentNotFoundError

class DeleteCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int):
        try:
            await self.repo.delete(comment_id)
            return {"detail": f"Комментарий с ID {comment_id} успешно удален"}
        except RecordNotFound:
            raise CommentNotFoundError(comment_id)