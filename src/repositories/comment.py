from sqlalchemy import select, delete, update
from datetime import datetime
from src.models import CommentModel
from src.repositories.base import BaseRepository
from src.exceptions.database_exceptions import RecordNotFound

class CommentRepository(BaseRepository):
    async def get_all(self):
        query = select(CommentModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_post(self, post_id: int):
        query = select(CommentModel).where(CommentModel.post_id == post_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, comment_id: int):
        query = select(CommentModel).where(CommentModel.id == comment_id)
        result = await self.session.execute(query)
        comment = result.scalar_one_or_none()
        
        if not comment:
            raise RecordNotFound(model="Comment", id_value=comment_id)
        return comment

    async def create(self, comment_data: dict):
        if "created_at" not in comment_data:
            comment_data["created_at"] = datetime.now()
        new_comment = CommentModel(**comment_data)
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        return new_comment

    async def update(self, comment_id: int, update_data: dict):
        await self.get_by_id(comment_id)

        clean_data = {k: v for k, v in update_data.items() if v is not None}
        if clean_data:
            query = (
                update(CommentModel)
                .where(CommentModel.id == comment_id)
                .values(**clean_data)
            )
            await self.session.execute(query)
            await self.session.commit()
            
        return await self.get_by_id(comment_id)

    async def delete(self, comment_id: int):
        await self.get_by_id(comment_id)
        
        query = delete(CommentModel).where(CommentModel.id == comment_id)
        await self.session.execute(query)
        await self.session.commit()
        return True