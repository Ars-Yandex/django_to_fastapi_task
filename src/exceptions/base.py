class AppError(Exception):
    def __init__(self, message: str, status_code: int = 500, **kwargs):
        self.message = message
        self.status_code = status_code
        self.extra = kwargs
        super().__init__(self.message)