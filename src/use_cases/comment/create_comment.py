from src.repositories.comment import CommentRepository
from src.repositories.post import PostRepository
from src.repositories.user import UserRepository
from src.exceptions.database_exceptions import RecordNotFound
from src.exceptions.domain_exceptions import PostNotFoundError

class CreateCommentUseCase:
    def __init__(self, repo: CommentRepository, post_repo: PostRepository, user_repo: UserRepository):
        self.repo = repo
        self.post_repo = post_repo
        self.user_repo = user_repo

    async def execute(self, data: dict):
        try:
            await self.post_repo.get_by_id(data["post_id"])
            return await self.repo.create(data)
            
        except RecordNotFound as e:
            if e.model == "Post":
                raise PostNotFoundError(post_id=data["post_id"])
            raise