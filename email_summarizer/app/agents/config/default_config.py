import os

DEFAULT_CONFIG = {
    "results_dir": os.getenv("EMAIL_SUMMARIZER_RESULTS_DIR", "./results"),
    # LLM settings
    "llm_provider": "azureopenai",
    "deep_think_llm": "o1",
    "quick_think_llm": "gpt-4.1",
    "backend_url": "https://angzou-openai-eastus2.openai.azure.com/",
    "api_version": "2024-12-01-preview",
    "temperature": 0.0,
    # Tool settings
    "online_tools": True,
}
