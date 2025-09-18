import os
import yaml
from typing import Any, Dict
from email_summarizer.app.agents.config.default_config import DEFAULT_CONFIG
from email_summarizer.app.utils.logging_init import get_logger

logger = get_logger("config_manager")

class ConfigManager:
    def __init__(self, config_path: str = None):
        self.default_config = DEFAULT_CONFIG.copy()
        # 支持 config.yaml 或 config.yml，优先 yaml
        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../config"))
        yaml_path = os.path.join(config_dir, "config.yaml")
        yml_path = os.path.join(config_dir, "config.yml")
        if config_path:
            self.config_path = config_path
        elif os.path.exists(yaml_path):
            self.config_path = yaml_path
        elif os.path.exists(yml_path):
            self.config_path = yml_path
        else:
            self.config_path = yaml_path  # 默认优先 yaml
        logger.info(f"Using configuration file: {self.config_path}")
        self.config = self._load_and_merge_config()

    def _load_yaml_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
                return data if data else {}
            except Exception as e:
                raise RuntimeError(f"Failed to load config file {self.config_path}: {e}")

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        merged = base.copy()
        for k, v in override.items():
            if isinstance(v, dict) and k in merged and isinstance(merged[k], dict):
                merged[k] = self._merge_configs(merged[k], v)
            else:
                merged[k] = v
        return merged

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """
        校验配置：无论 config.yml 是否存在，只校验 llm_provider、deep_think_llm、quick_think_llm、backend_url 四个字段必须存在
        """
        required_keys = ["deep_think_llm", "quick_think_llm"]
        missing = [k for k in required_keys if k not in config]
        if missing:
            raise ValueError(f"配置缺少必要字段: {missing}")

    def _load_and_merge_config(self) -> Dict[str, Any]:
        yaml_config = self._load_yaml_config()
        merged = self._merge_configs(self.default_config, yaml_config)
        self._validate_config(merged)
        return merged

    def get_config(self) -> Dict[str, Any]:
        return self.config
