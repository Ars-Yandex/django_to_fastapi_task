from src.repositories.user import UserRepository
from src.schemas.users import UserUpdate
from src.exceptions.database_exceptions import RecordNotFound, AlreadyExists
from src.exceptions.domain_exceptions import (
    UserNotFoundError, 
    UserAlreadyExistsError,
    EmailAlreadyExistsError,
    ForbiddenError
)

class UpdateUserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, user_id: int, update_data: UserUpdate, current_user):
        if current_user.id != user_id:
            raise ForbiddenError("Вы можете редактировать только собственный профиль")

        data = update_data.model_dump(exclude_unset=True)
        
        try:
            return await self.repo.update(user_id, data)
        except RecordNotFound:
            raise UserNotFoundError(user_id)
        except AlreadyExists as e:
            if e.field == "username":
                raise UserAlreadyExistsError(data["username"])
            if e.field == "email":
                raise EmailAlreadyExistsError(data["email"])
            raise