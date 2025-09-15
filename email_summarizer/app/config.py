import os
from dotenv import load_dotenv
from pathlib import Path
from email_summarizer.app.utils.config_manager import ConfigManager

# Load .env file from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

_agent_config = ConfigManager().get_config()

class Config:
    # Exchange
    EXCHANGE_EMAIL = os.getenv("EXCHANGE_EMAIL")
    EXCHANGE_USERNAME = os.getenv("EXCHANGE_USERNAME")
    EXCHANGE_PASSWORD = os.getenv("EXCHANGE_PASSWORD")
    EXCHANGE_SERVER = os.getenv("EXCHANGE_SERVER")

    # Azure OpenAI
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    
    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "Asia/Shanghai")

    # Report
    REPORT_RECIPIENT = os.getenv("REPORT_RECIPIENT")
    REPORT_TIME = os.getenv("REPORT_TIME", "08:00")

    # Langgraph
    LANGGRAPH_CONFIG = os.getenv("LANGGRAPH_CONFIG")

    # Agent/LLM/Tool config (from config_manager)
    RESULTS_DIR = _agent_config.get("results_dir")
    LLM_PROVIDER = _agent_config.get("llm_provider")
    DEEP_THINK_LLM = _agent_config.get("deep_think_llm")
    QUICK_THINK_LLM = _agent_config.get("quick_think_llm")
    BACKEND_URL = _agent_config.get("backend_url")
    API_VERSION = _agent_config.get("api_version", "2024-12-01-preview")
    TEMPERATURE = _agent_config.get("temperature", 0.0)
    ONLINE_TOOLS = _agent_config.get("online_tools", True)

    @classmethod
    def as_dict(cls):
        # 返回所有大写字段（环境变量和 config 字段）
        return {k: getattr(cls, k) for k in dir(cls) if k.isupper()}
