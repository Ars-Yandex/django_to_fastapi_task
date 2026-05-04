from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.database import get_db
from src.repositories.user import UserRepository
from src.services.auth_service import AuthService
from src.exceptions.domain_exceptions import ForbiddenError # Импортируем твою ошибку

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session = Depends(get_db)
):
    auth_service = AuthService()
    user_repo = UserRepository(session)
    
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен или срок действия истек",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не содержит идентификатор пользователя",
        )
    
    try:
        user = await user_repo.get_by_id(int(user_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
        
    return user

async def get_current_admin(current_user = Depends(get_current_user)):
    if not getattr(current_user, "is_superuser", False):
        raise ForbiddenError("Доступ запрещен. Это действие доступно только администратору")
        
    return current_user