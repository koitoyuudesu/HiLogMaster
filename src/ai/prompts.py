"""
提示词模板模块
管理 AI 分析的提示词
"""

# System Prompt
SYSTEM_PROMPT = """你是一名鸿蒙系统应用开发专家。请分析以下筛选出的 Hilog 错误日志片段。
背景：这些日志已经过预处理，仅包含特定包名的 Error 级别日志，不包含堆栈信息。
任务：
1. 归纳主要错误类型（如：网络错误、权限错误、数据解析错误等）。
2. 提取出现频率最高的 errorCode 和 errorMessage。
3. 推测可能的业务原因。
4. 生成一个简短的文件夹命名建议（格式：YYYYMMDD_包名_核心问题，不含特殊字符）。"""

# 分析提示词模板
ANALYSIS_PROMPT_TEMPLATE = """日志片段：
{filtered_logs}

请根据上述日志片段，提供详细的分析报告。"""

# 归档名生成提示词模板
ARCHIVE_NAME_PROMPT_TEMPLATE = """分析摘要：
{summary}

请根据上述分析摘要，生成一个合适的归档文件夹名称（格式：YYYYMMDD_包名_核心问题，不含特殊字符）。"""