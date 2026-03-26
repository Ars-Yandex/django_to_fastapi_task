from fastapi import HTTPException
from src.repositories.comment import CommentRepository

class GetCommentByIdUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int):
        comment = await self.repo.get_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment