from fastapi import HTTPException
from src.repositories.comment import CommentRepository

class DeleteCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_id: int):
        db_comment = await self.repo.get_by_id(comment_id)
        if not db_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
            
        await self.repo.delete(comment_id)
        return {"detail": "Comment deleted"}