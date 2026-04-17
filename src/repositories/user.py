from sqlalchemy import select, update, delete
from datetime import datetime
from src.models import UserModel
from src.repositories.base import BaseRepository
from src.exceptions.database_exceptions import RecordNotFound, AlreadyExists

class UserRepository(BaseRepository):
    async def get_all(self):
        query = select(UserModel)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise RecordNotFound(model="User", id_value=user_id)
        return user

    async def get_by_username(self, username: str):
        query = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_email(self, email: str):
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, user_data: dict):
        if await self.get_by_username(user_data.get("username")):
            raise AlreadyExists(model="User", field="username")
        
        if await self.get_by_email(user_data.get("email")):
            raise AlreadyExists(model="User", field="email")

        if "date_joined" not in user_data:
            user_data["date_joined"] = datetime.now()
            
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def update(self, user_id: int, update_data: dict):
        current_user = await self.get_by_id(user_id)

        clean_data = {k: v for k, v in update_data.items() if v is not None}
        
        if not clean_data:
            return current_user

        new_email = clean_data.get("email")
        if new_email and new_email != current_user.email:
            existing_user = await self.get_by_email(new_email)
            if existing_user:
                raise AlreadyExists(model="User", field="email")

        new_username = clean_data.get("username")
        if new_username and new_username != current_user.username:
            if await self.get_by_username(new_username):
                raise AlreadyExists(model="User", field="username")

        query = (
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(**clean_data)
        )
        await self.session.execute(query)
        await self.session.commit()
            
        await self.session.refresh(current_user)
        return current_user

    async def delete(self, user_id: int):
        await self.get_by_id(user_id)
        query = delete(UserModel).where(UserModel.id == user_id)
        await self.session.execute(query)
        await self.session.commit()
        return True