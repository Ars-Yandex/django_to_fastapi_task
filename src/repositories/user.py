from sqlalchemy import select, update, delete
from datetime import datetime
from src.models import UserModel
from src.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    async def get_all(self):
        query = select(UserModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_data: dict):
        if "date_joined" not in user_data:
            user_data["date_joined"] = datetime.now()
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update(self, user_id: int, update_data: dict):
        clean_data = {k: v for k, v in update_data.items() if v is not None}
        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**clean_data)
        )
        await self.session.execute(query)
        await self.session.commit()
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int):
        query = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(query)
        await self.session.commit()
        return True