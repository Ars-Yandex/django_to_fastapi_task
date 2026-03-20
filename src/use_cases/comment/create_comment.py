from fastapi import HTTPException, status
from src.repositories.comment import CommentRepository
from src.repositories.post import PostRepository
from src.repositories.user import UserRepository
from src.schemas.comments import CommentCreate

class CreateCommentUseCase:
    def __init__(
        self, 
        repo: CommentRepository, 
        post_repo: PostRepository, 
        user_repo: UserRepository
    ):
        self.repo = repo
        self.post_repo = post_repo
        self.user_repo = user_repo

    async def execute(self, comment_data: CommentCreate):
        data = comment_data.model_dump()
        
        post = await self.post_repo.get_by_id(data["post_id"])
        if not post:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Post with id {data['post_id']} not found"
            )

        author = await self.user_repo.get_by_id(data["author_id"])
        if not author:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"User with id {data['author_id']} not found"
            )

        return await self.repo.create(data)