from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import settings

DB_URL = settings.get_db_url()

engine = create_async_engine(url=DB_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine)


async def get_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
