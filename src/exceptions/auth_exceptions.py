from .base import AppError

class AuthError(AppError):
    def __init__(self, message: str):
        super().__init__(message, status_code=401)

class InvalidTokenError(AuthError):
    def __init__(self):
        super().__init__("Невалидный токен или срок действия истек")

class UserIDNotFoundError(AuthError):
    def __init__(self):
        super().__init__("Токен не содержит идентификатор пользователя")

class UserAuthNotFoundError(AuthError):
    def __init__(self):
        super().__init__("Пользователь не найден")