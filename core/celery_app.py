from celery import Celery
from core import config

app = Celery(
    "spartan_celery",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL,
    include=["core.tasks"]
)

# Optional context for future configurations
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
