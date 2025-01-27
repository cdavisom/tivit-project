from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.shared.base_config import settings

async_engine = create_async_engine(str(settings.POSTGRES_URL), echo=True, future=True)


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(async_engine)

    async with async_session() as session:
        yield session
