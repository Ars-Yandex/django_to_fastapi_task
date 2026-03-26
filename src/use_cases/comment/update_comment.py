from fastapi import HTTPException
from src.repositories.comment import CommentRepository
from src.schemas.comments import CommentUpdate

class UpdateCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int, update_data: CommentUpdate):
        db_comment = await self.repo.get_by_id(comment_id)
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        return await self.repo.update(comment_id, update_data.model_dump())