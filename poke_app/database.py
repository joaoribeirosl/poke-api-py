from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
