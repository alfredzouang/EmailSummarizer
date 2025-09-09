import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    # Exchange
    EXCHANGE_EMAIL = os.getenv("EXCHANGE_EMAIL")
    EXCHANGE_USERNAME = os.getenv("EXCHANGE_USERNAME")
    EXCHANGE_PASSWORD = os.getenv("EXCHANGE_PASSWORD")
    EXCHANGE_SERVER = os.getenv("EXCHANGE_SERVER")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "Asia/Shanghai")

    # Report
    REPORT_RECIPIENT = os.getenv("REPORT_RECIPIENT")
    REPORT_TIME = os.getenv("REPORT_TIME", "08:00")

    # Langgraph
    LANGGRAPH_CONFIG = os.getenv("LANGGRAPH_CONFIG")

    @classmethod
    def as_dict(cls):
        return {k: getattr(cls, k) for k in dir(cls) if k.isupper()}
