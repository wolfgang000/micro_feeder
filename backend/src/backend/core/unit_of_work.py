from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import Config
from backend.core import models


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subscription: models.Subscription) -> models.Subscription:
        subscription.inserted_at = datetime.now()
        self.session.add(subscription)
        await self.session.flush()
        return subscription


class SqlAlchemyUnitOfWork:
    ENGINE = create_async_engine(
        Config.DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1),
        pool_size=Config.DB_POOL_SIZE,
    )

    SESSION_FACTORY = async_sessionmaker(
        bind=ENGINE, autocommit=False, expire_on_commit=False, autoflush=False
    )

    def __init__(self, session_factory=SESSION_FACTORY):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.subscription_repo = SubscriptionRepository(self.session)
        return self

    async def __aexit__(self, *args):
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
