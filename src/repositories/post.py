from sqlalchemy import select, update, delete
from datetime import datetime
from sqlalchemy.orm import joinedload
from src.models import PostModel
from src.repositories.base import BaseRepository
from src.exceptions.database_exceptions import RecordNotFound

class PostRepository(BaseRepository):
    async def get_all(self):
        query = select(PostModel).options(
            joinedload(PostModel.author),
            joinedload(PostModel.location),
            joinedload(PostModel.category)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, post_id: int):
        query = (
            select(PostModel)
            .where(PostModel.id == post_id)
            .options(
                joinedload(PostModel.author),
                joinedload(PostModel.location),
                joinedload(PostModel.category)
            )
        )
        result = await self.session.execute(query)
        post = result.scalar_one_or_none()
        
        if not post:
            raise RecordNotFound(model="Post", id_value=post_id)
        return post

    async def create(self, post_data: dict, author_id: int):
        clean_data = {k: v for k, v in post_data.items() if v is not None}
        if "created_at" not in clean_data:
            clean_data["created_at"] = datetime.now()
            
        new_post = PostModel(**clean_data, author_id=author_id)
        self.session.add(new_post)
        await self.session.commit()
        
        return await self.get_by_id(new_post.id)

    async def update(self, post_id: int, update_data: dict):
        await self.get_by_id(post_id)

        clean_data = {k: v for k, v in update_data.items() if v is not None}
        
        if clean_data:
            query = (
                update(PostModel)
                .where(PostModel.id == post_id)
                .values(**clean_data)
            )
            await self.session.execute(query)
            await self.session.commit()
            
        return await self.get_by_id(post_id)

    async def delete(self, post_id: int):
        await self.get_by_id(post_id)

        query = delete(PostModel).where(PostModel.id == post_id)
        await self.session.execute(query)
        await self.session.commit()
        return True