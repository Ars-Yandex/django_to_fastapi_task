from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session