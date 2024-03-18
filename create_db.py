import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.conf.config import settings

async def create_tables():
    engine = create_async_engine(settings.postgres_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())
