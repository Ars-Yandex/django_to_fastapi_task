from datetime import datetime
from sqlalchemy import select, update, delete
from src.models import LocationModel
from src.repositories.base import BaseRepository
from src.exceptions.database_exceptions import RecordNotFound

class LocationRepository(BaseRepository):
    async def get_all(self):
        query = select(LocationModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, loc_id: int):
        query = select(LocationModel).where(LocationModel.id == loc_id)
        result = await self.session.execute(query)
        location = result.scalar_one_or_none()
        
        if not location:
            raise RecordNotFound(model="Location", id_value=loc_id)
        return location

    async def get_by_name(self, name: str):
        query = select(LocationModel).where(LocationModel.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, loc_data: dict):
        if "created_at" not in loc_data:
            loc_data["created_at"] = datetime.now()
            
        new_loc = LocationModel(**loc_data)
        self.session.add(new_loc)
        await self.session.commit()
        await self.session.refresh(new_loc)
        return new_loc

    async def update(self, loc_id: int, update_data: dict):
        await self.get_by_id(loc_id)

        clean_data = {k: v for k, v in update_data.items() if v is not None}
        if clean_data:
            query = (
                update(LocationModel)
                .where(LocationModel.id == loc_id)
                .values(**clean_data)
            )
            await self.session.execute(query)
            await self.session.commit()
        
        return await self.get_by_id(loc_id)

    async def delete(self, loc_id: int):
        # Проверяем наличие перед удалением
        await self.get_by_id(loc_id)
        
        query = delete(LocationModel).where(LocationModel.id == loc_id)
        await self.session.execute(query)
        await self.session.commit()
        return True