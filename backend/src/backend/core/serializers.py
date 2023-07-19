from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class SubscriptionRequest(BaseModel):
    webhook_url: AnyHttpUrl
    feed_url: AnyHttpUrl


class SubscriptionResponse(BaseModel):
    id: int
    webhook_url: str
    feed_url: str
    inserted_at: str


class FeedEntryWebhookRequest(BaseModel):
    id: Optional[str] = None
    link: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    published_at: Optional[str] = None
