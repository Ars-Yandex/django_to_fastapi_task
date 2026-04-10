from .base import AppError

class RecordNotFound(AppError):
    def __init__(self, model: str, id_value: any):
        self.model = model
        self.id_value = id_value
        self.message = f"Запись в {model} с ID {id_value} не найдена"
        super().__init__(self.message)

class AlreadyExists(AppError):
    def __init__(self, model: str, field: str):
        self.model = model
        self.field = field
        self.message = f"{model} с таким {field} уже существует"
        super().__init__(self.message)