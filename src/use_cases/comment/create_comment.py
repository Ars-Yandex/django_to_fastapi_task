from src.repositories.comment import CommentRepository
from src.schemas.comments import CommentCreate

class CreateCommentUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self, comment_data: CommentCreate, author_id: int):
        data = comment_data.model_dump()
        data["author_id"] = author_id
        return await self.repo.create(data)