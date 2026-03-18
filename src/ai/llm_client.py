"""
LLM 客户端模块
调用 Ollama API 进行日志分析
"""

import requests
from typing import Optional
from config import Config


class LLMClient:
    """LLM 客户端"""

    def __init__(self):
        self.base_url = Config.OLLAMA_BASE_URL
        self.api_key = Config.OLLAMA_API_KEY
        self.model = Config.LLM_MODEL

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        调用 LLM 生成文本

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词

        Returns:
            生成的文本
        """
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            payload["system"] = system_prompt

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()
        return result.get("response", "")

    def analyze_logs(self, filtered_logs: str) -> str:
        """
        分析筛选后的日志

        Args:
            filtered_logs: 筛选后的日志文本

        Returns:
            分析摘要
        """
        from src.ai.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT_TEMPLATE

        prompt = ANALYSIS_PROMPT_TEMPLATE.format(filtered_logs=filtered_logs)
        return self.generate(prompt, system_prompt=SYSTEM_PROMPT)

    def suggest_archive_name(self, summary: str) -> str:
        """
        生成归档文件夹名称建议

        Args:
            summary: 分析摘要

        Returns:
            归档文件夹名称
        """
        from src.ai.prompts import SYSTEM_PROMPT, ARCHIVE_NAME_PROMPT_TEMPLATE

        prompt = ARCHIVE_NAME_PROMPT_TEMPLATE.format(summary=summary)
        return self.generate(prompt, system_prompt=SYSTEM_PROMPT)