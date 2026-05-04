from src.repositories.comment import CommentRepository
from src.schemas.comments import CommentUpdate
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import CommentNotFoundError, ForbiddenError

class UpdateCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int, update_data: CommentUpdate, current_user_id: int):
        try:
            comment = await self.repo.get_by_id(comment_id)
            
            if comment.author_id != current_user_id:
                raise ForbiddenError("Вы не можете редактировать чужой комментарий")
            
            data = update_data.model_dump(exclude_unset=True)
            return await self.repo.update(comment_id, data)
            
        except RecordNotFound:
            raise CommentNotFoundError(comment_id)