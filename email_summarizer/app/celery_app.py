from celery import Celery
from app.config import Config

celery_app = Celery(
    "email_summarizer",
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    timezone=Config.CELERY_TIMEZONE,
    enable_utc=True,
    beat_schedule={
        # Example: daily summary task, actual task name to be filled later
        # "daily_email_summary": {
        #     "task": "app.tasks.summarize.daily_summary",
        #     "schedule": crontab(hour=8, minute=0),
        #     "args": (),
        # },
    },
)

__all__ = ["celery_app"]
