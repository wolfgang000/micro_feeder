import datetime
from sqlalchemy import UniqueConstraint
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
    feed_last_entry_id: Mapped[str]
    updated_at: Mapped[datetime.datetime]
    inserted_at: Mapped[datetime.datetime]

    def __init__(self, webhook_url: str, feed_url: str):
        self.webhook_url = webhook_url
        self.feed_url = feed_url

    def __repr__(self) -> str:
        return f"Subscription(id={self.id!r}, webhook_url={self.webhook_url!r}, feed_url={self.feed_url!r})"


class User(Base):
    __tablename__ = "app_user"
    __table_args__ = (UniqueConstraint("email", name="app_user_email_index"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    updated_at: Mapped[datetime.datetime]
    inserted_at: Mapped[datetime.datetime]

    def __init__(self, email: str):
        self.email = email

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"
