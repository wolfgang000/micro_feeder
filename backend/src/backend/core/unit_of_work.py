from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import Config
from backend.core import models


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subscription: models.Subscription) -> models.Subscription:
        subscription.inserted_at = datetime.utcnow()
        subscription.updated_at = datetime.utcnow()
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    async def update(self, subscription: models.Subscription) -> models.Subscription:
        subscription.updated_at = datetime.utcnow()
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    async def update_by_id(self, id: int, values: Dict[str, Any]):
        values["updated_at"] = datetime.utcnow()
        await self.session.execute(
            update(models.Subscription)
            .where(models.Subscription.id == id)
            .values(values)
        )

    async def list(self):
        return await self.session.execute(select(models.Subscription))


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
