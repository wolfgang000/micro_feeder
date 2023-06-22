from celery import Celery
from backend.config import Config

app = Celery(
    "proj",
    broker=Config.RABBITMQ_URL,
    backend=Config.REDIS_URL,
    include=["backend.celery.tasks"],
)

app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "backend.celery.tasks.schedule_fetch_feeds",
        "schedule": 60.0,
    },
}

if __name__ == "__main__":
    app.start()
