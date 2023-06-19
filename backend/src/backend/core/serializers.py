from pydantic import BaseModel


class Subscription(BaseModel):
    webhook_url: str
    feed_url: str
