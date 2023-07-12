from pydantic import BaseModel, AnyHttpUrl


class SubscriptionRequest(BaseModel):
    webhook_url: AnyHttpUrl
    feed_url: AnyHttpUrl


class SubscriptionResponse(BaseModel):
    id: int
    webhook_url: str
    feed_url: str
    inserted_at: str
