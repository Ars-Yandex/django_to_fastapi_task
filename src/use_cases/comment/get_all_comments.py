from src.repositories.comment import CommentRepository

class GetAllCommentsUseCase:
    def __init__(self, repo: CommentRepository):
        self.repo = repo

    async def execute(self):
        return await self.repo.get_all()