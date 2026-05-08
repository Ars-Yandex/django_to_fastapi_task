from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.database import get_db
from src.repositories.user import UserRepository
from src.services.auth_service import AuthService
from src.exceptions.domain_exceptions import ForbiddenError
from src.exceptions.auth_exceptions import (
    InvalidTokenError, 
    UserIDNotFoundError, 
    UserAuthNotFoundError
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session = Depends(get_db)
):
    auth_service = AuthService()
    user_repo = UserRepository(session)
    
    payload = auth_service.decode_token(token)
    if not payload:
        raise InvalidTokenError()
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise UserIDNotFoundError()
    
    try:
        user = await user_repo.get_by_id(int(user_id))
        if user is None:
            raise UserAuthNotFoundError()
    except (Exception, ValueError):
        raise UserAuthNotFoundError()
        
    return user

async def get_current_admin(current_user = Depends(get_current_user)):
    if not getattr(current_user, "is_superuser", False):
        raise ForbiddenError("Доступ запрещен. Это действие доступно только администратору")
        
    return current_user