from typing import Type, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from config import Config

Base = declarative_base()


def session_factory(config: Type[Config]) -> sessionmaker:
    engine = create_engine(config.db_uri)

    return sessionmaker(engine)


def async_session_factory(config: Type[Config]) -> Tuple[sessionmaker, AsyncEngine]:
    engine = create_async_engine(config.async_db_uri)

    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession), engine
