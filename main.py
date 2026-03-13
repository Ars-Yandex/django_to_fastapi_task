import asyncio
import uvicorn

from src.app import create_app
from src.api.posts import router as post_router
from src.api.category import router as category_router
from src.api.location import router as location_router
from src.api.users import router as user_router
from src.api.comment import router as comment_router
app = create_app()
app.include_router(post_router)
app.include_router(category_router)
app.include_router(location_router)
app.include_router(user_router)
app.include_router(comment_router)


async def run() -> None:
    config = uvicorn.Config(
        "main:app", host="127.0.0.1", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
