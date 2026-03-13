from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.posts import router as post_router
from src.api.category import router as category_router
from src.api.location import router as location_router
from src.api.users import router as user_router
from src.api.comment import router as comment_router

def create_app() -> FastAPI:
    app = FastAPI(title="Yatube FastAPI Migration") 
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(post_router)
    app.include_router(category_router)
    app.include_router(location_router)
    app.include_router(user_router)
    app.include_router(comment_router)

    return app