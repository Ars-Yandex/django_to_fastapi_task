from src.repositories.comment import CommentRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import CommentNotFoundError

class GetCommentByIdUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int):
        try:
            return await self.repo.get_by_id(comment_id)
        except RecordNotFound:
            raise CommentNotFoundError(comment_id)