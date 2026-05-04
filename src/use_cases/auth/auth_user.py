from src.repositories.user import UserRepository
from src.services.auth_service import AuthService

class AuthenticateUserUseCase:
    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        
        if not user:
            return None
            
        if not self.auth_service.verify_password(password, user.password):
            return None
            
        await self.user_repo.update_last_login(user.id)
        return user