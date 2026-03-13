from sqlalchemy import select, update, delete
from datetime import datetime
from src.models import CategoryModel
from src.repositories.base import BaseRepository

class CategoryRepository(BaseRepository):
    async def get_all(self):
        query = select(CategoryModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, cat_id: int):
        query = select(CategoryModel).where(CategoryModel.id == cat_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, cat_data: dict):
        if "created_at" not in cat_data:
            cat_data["created_at"] = datetime.now()
        new_cat = CategoryModel(**cat_data)
        self.session.add(new_cat)
        await self.session.commit()
        await self.session.refresh(new_cat)
        return new_cat

    async def update(self, cat_id: int, update_data: dict):
        clean_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not clean_data:
            return await self.get_by_id(cat_id)

        query = (
            update(CategoryModel)
            .where(CategoryModel.id == cat_id)
            .values(**clean_data)
        )
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_by_id(cat_id)

    async def delete(self, cat_id: int):
        query = delete(CategoryModel).where(CategoryModel.id == cat_id)
        await self.session.execute(query)
        await self.session.commit()
        return True