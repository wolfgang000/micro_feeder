from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any
from result import Err, Ok, Result
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from backend.config import Config
from backend.core import models


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, subscription: models.Subscription) -> models.Subscription:
        subscription.inserted_at = datetime.now(timezone.utc)
        subscription.updated_at = datetime.now(timezone.utc)
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    async def update(self, subscription: models.Subscription) -> models.Subscription:
        subscription.updated_at = datetime.now(timezone.utc)
        self.session.add(subscription)
        await self.session.flush()
        return subscription

    async def update_by_id(self, id: int, values: Dict[str, Any]):
        values["updated_at"] = datetime.now(timezone.utc)
        await self.session.execute(
            update(models.Subscription)
            .where(models.Subscription.id == id)
            .values(values)
        )

    async def list_by_user_id(self, user_id: int):
        return await self.session.execute(
            select(models.Subscription).where(models.Subscription.user_id == user_id)
        )

    async def list(self):
        return await self.session.execute(select(models.Subscription))

    async def get_by_id_and_user_id(
        self, id: int, user_id: int
    ) -> Result[models.Subscription, str]:
        query = select(models.Subscription).where(
            models.Subscription.id == id and models.Subscription.user_id == user_id
        )
        result = await self.session.execute(query)
        try:
            (subscription,) = result.one()
            return Ok(subscription)

        except NoResultFound:
            return Err("NoResultFound")

    async def delete_by_id(self, id: int):
        query = delete(models.Subscription).where(models.Subscription.id == id)
        await self.session.execute(query)
        await self.session.flush()


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: models.User) -> models.User:
        user.inserted_at = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user: models.User) -> models.User:
        user.updated_at = datetime.now(timezone.utc)
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_by_id(self, id: int, values: Dict[str, Any]):
        values["updated_at"] = datetime.now(timezone.utc)
        await self.session.execute(
            update(models.User).where(models.User.id == id).values(values)
        )

    async def get_by_email(self, email: str) -> Result[models.User, str]:
        query = select(models.User).where(models.User.email == email)
        result = await self.session.execute(query)
        try:
            (user,) = result.one()
            return Ok(user)

        except NoResultFound:
            return Err("NoResultFound")

    async def get_by_id(self, id: int) -> Result[models.User, str]:
        query = select(models.User).where(models.User.id == id)
        result = await self.session.execute(query)
        try:
            (user,) = result.one()
            return Ok(user)

        except NoResultFound:
            return Err("NoResultFound")


class SqlAlchemyUnitOfWork:
    ENGINE = create_async_engine(
        Config.DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1),
        pool_size=Config.DB_POOL_SIZE,
        connect_args={"options": "-c timezone=utc"},
    )

    SYNC_ENGINE = create_engine(
        Config.DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1),
        pool_size=Config.DB_POOL_SIZE,
        connect_args={"options": "-c timezone=utc"},
    )

    SESSION_FACTORY = async_sessionmaker(
        bind=ENGINE,
        autocommit=False,
        expire_on_commit=False,
        autoflush=False,
    )

    SYNC_SESSION_FACTORY = sessionmaker(
        bind=SYNC_ENGINE,
        autocommit=False,
        expire_on_commit=False,
        autoflush=False,
    )

    def __init__(
        self, session_factory=SESSION_FACTORY, sync_session_factory=SYNC_SESSION_FACTORY
    ):
        self.session_factory = session_factory
        self.sync_session_factory = sync_session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.subscription_repo = SubscriptionRepository(self.session)
        self.user_repo = UserRepository(self.session)
        return self

    async def __aexit__(self, *args):
        task = asyncio.create_task(self.session.close())
        await asyncio.shield(task)

    def __enter__(self):
        self.sync_session = self.sync_session_factory()
        return self

    def __exit__(self, *args):
        self.sync_session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
