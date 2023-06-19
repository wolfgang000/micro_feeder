from __future__ import annotations
import abc
import asyncio
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import Config

class AbstractUnitOfWork(abc.ABC):
    session: AsyncSession

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError



class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    ENGINE = create_async_engine(
        Config.DATABASE_URL,
        pool_size=Config.DB_POOL_SIZE,
    )

    SESSION_FACTORY = async_sessionmaker(
        bind=ENGINE, autocommit=False, expire_on_commit=False
    )

    def __init__(self, session_factory=SESSION_FACTORY):
        self.session_factory = session_factory

    async def  __aenter__(self):
        uow = super().__aenter__()
        self.session = self.session_factory()
        return uow

    async def __aexit__(self, *args):
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)
        

    async def commit(self):
        self.session.commit()

    async def rollback(self):
        self.session.rollback()
