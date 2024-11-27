from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..settings import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine)
