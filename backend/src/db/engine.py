from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.core.config import settings

DATABASE_URL = settings.DATABASE_URI

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
