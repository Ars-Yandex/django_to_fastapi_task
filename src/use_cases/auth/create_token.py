from src.services.auth_service import AuthService

class CreateTokenUseCase:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def execute(self, user) -> str:
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email
        }
        return self.auth_service.create_access_token(data=token_data)