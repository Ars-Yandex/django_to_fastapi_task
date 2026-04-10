import logging
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from src.api.posts import router as post_router
from src.api.category import router as category_router
from src.api.location import router as location_router
from src.api.users import router as user_router
from src.api.comment import router as comment_router
from src.exceptions.domain_exceptions import DomainError

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE)
    ]
)

logger = logging.getLogger("uvicorn.error")

def create_app() -> FastAPI:
    app = FastAPI(title="Yatube FastAPI Migration") 
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        """Обработка бизнес-ошибок (404, 409, 400)."""
        message_lc = exc.message.lower()
        
        if "не найден" in message_lc:
            status_code = status.HTTP_404_NOT_FOUND
        elif any(word in message_lc for word in ["уже существует", "занят", "занята"]):
            status_code = status.HTTP_409_CONFLICT
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            
        return JSONResponse(
            status_code=status_code,
            content={"detail": exc.message}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Возвращает только список понятных сообщений об ошибках."""
        errors = exc.errors()
        error_messages = [err.get("msg") for err in errors]
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": error_messages}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Критический перехват всего остального."""
        logger.error(f"Критическая ошибка на {request.url.path}: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Произошла неизвестная ошибка. Мы уже работаем над её исправлением."}
        )

    app.include_router(post_router)
    app.include_router(category_router)
    app.include_router(location_router)
    app.include_router(user_router)
    app.include_router(comment_router)

    return app