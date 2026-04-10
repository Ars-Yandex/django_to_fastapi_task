from src.repositories.user import UserRepository
from src.schemas.users import UserCreate
from src.exceptions.database_exceptions import AlreadyExists
from src.exceptions.domain_exceptions import UserAlreadyExistsError, EmailAlreadyExistsError

class CreateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_data: UserCreate):
        try:
            return await self.repo.create(user_data.model_dump())
        except AlreadyExists as e:
            if e.field == "username":
                raise UserAlreadyExistsError(user_data.username)
            if e.field == "email":
                raise EmailAlreadyExistsError(user_data.email)
            raise