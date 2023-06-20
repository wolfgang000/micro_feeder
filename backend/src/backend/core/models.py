from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(primary_key=True)
    webhook_url: Mapped[str]
    feed_url: Mapped[str]

    def __init__(self, webhook_url: str, feed_url: str):
        self.webhook_url = webhook_url
        self.feed_url = feed_url

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, webhook_url={self.webhook_url!r}, feed_url={self.feed_url!r})"
