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

    # API Key    
    DEEP_THINK_LLM_KEY = os.getenv("DEEP_THINK_LLM_KEY")
    QUICK_THINK_LLM_KEY = os.getenv("QUICK_THINK_LLM_KEY")

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
    RESULTS_DIR = _agent_config.get("results_dir", "./results")

    DEEP_THINK_LLM_CONFIG = _agent_config.get("deep_think_llm", {})
    QUICK_THINK_LLM_CONFIG = _agent_config.get("quick_think_llm", {})

    DEEP_THINK_MODEL = DEEP_THINK_LLM_CONFIG.get("model", "o1")
    QUICK_THINK_MODEL = QUICK_THINK_LLM_CONFIG.get("model", "gpt-4.1")

    DEEP_THINK_API_VERSION = DEEP_THINK_LLM_CONFIG.get("api_version", "2024-12-01-preview")
    QUICK_THINK_API_VERSION = QUICK_THINK_LLM_CONFIG.get("api_version", "2024-12-01-preview")

    DEEP_THINK_BACKEND_URL = DEEP_THINK_LLM_CONFIG.get("backend_url", "https://tryaifoundry.openai.azure.com/")
    QUICK_THINK_BACKEND_URL = QUICK_THINK_LLM_CONFIG.get("backend_url", "https://tryaifoundry.openai.azure.com/")

    DEEP_THINK_PROVIDER = DEEP_THINK_LLM_CONFIG.get("llm_provider", "azureopenai")
    QUICK_THINK_PROVIDER = QUICK_THINK_LLM_CONFIG.get("llm_provider", "azureopenai")

    DEEP_THINK_TEMPERATURE = DEEP_THINK_LLM_CONFIG.get("temperature", 0.0)
    QUICK_THINK_TEMPERATURE = QUICK_THINK_LLM_CONFIG.get("temperature", 0.0)

    ONLINE_TOOLS = _agent_config.get("online_tools", True)

    @classmethod
    def as_dict(cls):
        # 返回所有大写字段（环境变量和 config 字段）
        return {k: getattr(cls, k) for k in dir(cls) if k.isupper()}
