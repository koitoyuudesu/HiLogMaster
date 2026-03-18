"""
配置工具模块
提供配置加载和验证功能
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from config import Config


class ConfigLoader:
    """配置加载器"""

    @staticmethod
    def load_from_env() -> Dict[str, Any]:
        """
        从环境变量加载配置

        Returns:
            配置字典
        """
        return {
            "ollama_base_url": os.getenv("OLLAMA_BASE_URL", Config.OLLAMA_BASE_URL),
            "ollama_api_key": os.getenv("OLLAMA_API_KEY", Config.OLLAMA_API_KEY),
            "llm_model": os.getenv("LLM_MODEL", Config.LLM_MODEL),
            "archive_root_dir": os.getenv("ARCHIVE_ROOT_DIR", str(Config.ARCHIVE_ROOT_DIR)),
            "context_lines": int(os.getenv("CONTEXT_LINES", str(Config.CONTEXT_LINES))),
        }

    @staticmethod
    def load_from_file(config_path: Path) -> Dict[str, Any]:
        """
        从配置文件加载配置

        Args:
            config_path: 配置文件路径

        Returns:
            配置字典
        """
        if not config_path.exists():
            return {}

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_to_file(config: Dict[str, Any], config_path: Path):
        """
        保存配置到文件

        Args:
            config: 配置字典
            config_path: 配置文件路径
        """
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """
        验证配置

        Args:
            config: 配置字典

        Returns:
            是否有效
        """
        required_keys = ["ollama_base_url", "llm_model"]
        for key in required_keys:
            if key not in config or not config[key]:
                return False
        return True