from sqlalchemy import create_engine

from aiogrambot.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(settings.get_db_url(), echo=True)

sync_engine = create_engine(settings.get_db_url())

async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass