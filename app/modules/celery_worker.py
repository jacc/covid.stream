# Celery worker for updating stats + pulling info.

from celery import Celery

application = Celery(
    "workers",
    broker="redis://localhost:6073/0",
    backend="redis://localhost:6073/1",
    include=["workers.update_numbers"],
)
