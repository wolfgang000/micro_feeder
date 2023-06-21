from celery import Celery

app = Celery(
    "proj",
    broker="pyamqp://guest@message_broker_dev//",
    backend="redis://message_broker_store_dev",
    include=["backend.celery.tasks"],
)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "backend.celery.tasks.add",
        "schedule": 30.0,
        "args": (16, 16),
    },
}

if __name__ == "__main__":
    app.start()
