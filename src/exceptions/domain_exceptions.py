from .base import AppError

class DomainError(AppError):
    """Базовый класс для ошибок бизнес-логики"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# --- Категории ---
class CategoryNotFoundError(DomainError):
    def __init__(self, entity_id: int):
        super().__init__(f"Категория с ID {entity_id} не найдена")

class CategoryAlreadyExistsError(DomainError):
    def __init__(self, slug: str):
        super().__init__(f"Категория со слагом '{slug}' уже существует")

# --- Пользователи ---
class UserNotFoundError(DomainError):
    def __init__(self, entity_id: int):
        super().__init__(f"Пользователь с ID {entity_id} не найден")

class UserAlreadyExistsError(DomainError):
    def __init__(self, username: str):
        super().__init__(f"Пользователь с логином '{username}' уже существует")

class EmailAlreadyExistsError(DomainError):
    def __init__(self, email: str):
        super().__init__(f"Пользователь с почтой '{email}' уже существует")

# --- Комментарии ---
class CommentNotFoundError(DomainError):
    def __init__(self, comment_id: int):
        super().__init__(f"Комментарий с ID {comment_id} не найден")

class CommentAccessDeniedError(DomainError):
    def __init__(self):
        super().__init__("У вас нет прав для редактирования или удаления этого комментария")

# --- Посты ---
class PostNotFoundError(DomainError):
    def __init__(self, post_id: int):
        super().__init__(f"Пост с ID {post_id} не найден")

# --- Локации ---
class LocationNotFoundError(DomainError):
    def __init__(self, entity_id: int):
        super().__init__(f"Локация с ID {entity_id} не найдена")

class LocationAlreadyExistsError(DomainError):
    def __init__(self, name: str):
        super().__init__(f"Локация с названием '{name}' уже существует")