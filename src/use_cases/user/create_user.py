from src.repositories.user import UserRepository
from src.schemas.users import UserCreate
from src.services.auth_service import AuthService
from src.exceptions.database_exceptions import AlreadyExists
from src.exceptions.domain_exceptions import UserAlreadyExistsError, EmailAlreadyExistsError

class CreateUserUseCase:
    def __init__(self, repo: UserRepository, auth_service: AuthService):
        self.repo = repo
        self.auth_service = auth_service

    async def execute(self, user_data: UserCreate):
        data = user_data.model_dump()
        
        raw_password = data.get("password")
        if raw_password:
            data["password"] = self.auth_service.hash_password(raw_password)
            
        try:
            return await self.repo.create(data)
        except AlreadyExists as e:
            if e.field == "username":
                raise UserAlreadyExistsError(user_data.username)
            if e.field == "email":
                raise EmailAlreadyExistsError(user_data.email)
            raise