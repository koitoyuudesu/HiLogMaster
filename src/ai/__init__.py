"""
AI 模块
提供 LLM 客户端和提示词模板
"""

from .llm_client import LLMClient
from .prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT_TEMPLATE, ARCHIVE_NAME_PROMPT_TEMPLATE

__all__ = [
    "LLMClient",
    "SYSTEM_PROMPT",
    "ANALYSIS_PROMPT_TEMPLATE",
    "ARCHIVE_NAME_PROMPT_TEMPLATE"
]