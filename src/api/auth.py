from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.repositories.user import UserRepository
from src.services.auth_service import AuthService
from src.use_cases.auth.auth_user import AuthenticateUserUseCase
from src.use_cases.auth.create_token import CreateTokenUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(session)
    auth_service = AuthService()
    
    auth_use_case = AuthenticateUserUseCase(user_repo, auth_service)
    user = await auth_use_case.execute(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )

    token_use_case = CreateTokenUseCase(auth_service)
    access_token = token_use_case.execute(user)

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }