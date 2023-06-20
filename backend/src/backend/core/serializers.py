from pydantic import BaseModel, HttpUrl


class SubscriptionRequest(BaseModel):
    webhook_url: HttpUrl
    feed_url: HttpUrl


class SubscriptionResponse(BaseModel):
    id: int
    webhook_url: str
    feed_url: str
