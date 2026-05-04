from src.repositories.comment import CommentRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import CommentNotFoundError, ForbiddenError

class DeleteCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int, current_user):
        try:
            comment = await self.repo.get_by_id(comment_id)
            
            if not current_user.is_superuser and comment.author_id != current_user.id:
                raise ForbiddenError("Вы не можете удалить чужой комментарий")

            await self.repo.delete(comment_id)
            return {"detail": f"Комментарий с ID {comment_id} успешно удален"}
            
        except RecordNotFound:
            raise CommentNotFoundError(comment_id)