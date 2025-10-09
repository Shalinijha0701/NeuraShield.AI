from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "neurashield",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        "app.tasks.analyze_code": {"queue": "analysis"},
        "app.tasks.scan_security": {"queue": "security"},
        "app.tasks.optimize_pipeline": {"queue": "optimization"},
    }
)