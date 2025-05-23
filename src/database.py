import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text

from src.config import settings


engine = create_async_engine(settings.db_url)

session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = session_maker()
