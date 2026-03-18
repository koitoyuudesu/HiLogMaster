# 项目名称：LogMaster AI (HarmonyOS Hilog 专用版)

## 1. 项目概述

**目标**：开发一个运行在 Windows 本地的桌面工具，专门用于处理鸿蒙系统 Hilog 日志文件的自动化解压、筛选、分析与归档。 **核心场景**：开发人员接收测试提供的 Hilog 压缩包或单文件，需要快速定位特定应用包名的错误日志，并归档记录。 **目标用户**：鸿蒙应用开发者、测试人员。 **开发语言**：Python 3.9+ **运行环境**：Windows 10/11 (本地运行)

## 2. 日志格式与结构说明 (关键约束)

**AI 开发需严格遵守以下日志特征：**

1. **文件结构**：
    - **压缩包**：解压后包含多层文件夹，核心日志位于名为 `hilog` 的子文件夹内。
    - **日志文件**：`hilog` 文件夹内包含多个 `.txt` 文件（按时间或模块分割），需遍历处理所有 txt 文件。
    - **单文件**：有时直接提供单个 `.txt` 日志文件。
2. **日志行格式**：
    - 典型格式：`MM-DD HH:MM:SS.mmm PID TID Level Tag: Content`
    - 示例：`03-09 20:03:26.404 50989 50989 E A00901/ei.hmos.accountcontactsservice/ACCOUNT_CONTACTS: [PosterCloudService]: setPosterAuthorizationIncre failed...`
    - **级别标识**：`E` 代表 Error 级别，是分析重点。不存在 Java/JS 堆栈信息。
    - **错误特征**：错误通常为业务逻辑错误（如 errorCode, errorMessage），由应用 try-catch 后打印。

## 3. 功能需求 (Functional Requirements)

### 3.1 核心工作流 (Core Workflow)

用户界面需提供输入框：**“目标包名/关键字”**（必填）。 用户拖入文件后，系统自动执行：

1. **文件预处理**：
    - 识别输入：若是 `.zip`，递归解压直到找到 `hilog` 文件夹；若是 `.txt`，直接读取。
    - 编码检测：自动识别 txt 文件编码（UTF-8 或 GBK），防止乱码。
    - **无需脱敏**：假设系统日志不含敏感个人信息，跳过脱敏步骤。
2. **日志筛选与提取 (关键步骤)**：
    - 遍历 `hilog` 目录下所有 `.txt` 文件。
    - **行级过滤**：仅读取包含 `E` (Error 级别) 的行。
    - **关键字过滤**：在 Error 行中，进一步筛选包含用户输入的“目标包名/关键字”的行。
    - **上下文提取**：对于匹配到的错误行，可选提取其前后各 1 行日志（作为上下文），若无上下文则只提取错误行。
    - 将筛选后的日志片段合并为一个临时文本。
3. **AI 智能分析**：
    - 将筛选后的日志片段发送给 LLM。
    - 生成分析摘要：错误类型、高频错误码、可能的业务原因。
    - 生成归档名：`日期_包名_核心问题摘要`。
4. **智能归档**：
    - 创建归档文件夹，将原始日志文件（或筛选后的日志）移动至此。
    - 生成 `analysis_report.md`，包含 AI 摘要和筛选出的错误日志原文。
5. **索引注册**：
    - 将归档信息、摘要、包名写入 SQLite。
    - 将摘要向量化存入 ChromaDB。

### 3.2 检索与回顾 (Search & Review)

- **搜索方式**：支持通过“包名”、“错误码”、“自然语言描述”搜索。
- **展示内容**：显示归档路径、AI 分析报告、错误日志片段。

### 3.3 配置管理 (Settings)

- **LLM 配置**：支持配置本地 Ollama 地址或 API Key。
- **默认关键字**：可预设常用的包名关键字，方便快速选择。
- **归档根目录**：设置日志存储路径。
- **上下文行数**：设置提取错误日志时包含的前后行数（默认 1 行）。

## 4. 非功能需求 (Non-Functional Requirements)

- **性能优化**：Hilog 文件可能很大（几百 MB），**严禁将整个文件读入内存**。必须使用流式读取 (Line-by-Line) 进行筛选。
- **准确性**：正则解析需准确识别 Hilog 的时间戳和级别，避免误判。
- **易用性**：GUI 需明确提示用户输入“包名/关键字”，否则无法开始分析。

## 5. 技术栈建议 (Tech Stack)

- **GUI 框架**：`CustomTkinter` (支持深色模式，现代感)。
- **文件处理**：`zipfile`, `chardet`, 原生 `open(..., encoding=...)` 流式读取。
- **文本解析**：`re` (正则表达式)。
- **LLM 交互**：`requests` (直接调用 Ollama API 即可，无需重型框架)。
- **向量数据库**：`chromadb` (本地持久化)。
- **数据库**：`sqlite3`。

## 6. 数据结构设计 (Data Schema)

### 6.1 SQLite 表：`log_records`

|字段名|类型|说明|
|:--|:--|:--|
|`id`|INTEGER|主键|
|`package_name`|TEXT|分析的包名/关键字|
|`file_path`|TEXT|归档后的绝对路径|
|`archive_name`|TEXT|生成的文件夹名|
|`summary`|TEXT|AI 生成的分析报告|
|`error_count`|INTEGER|筛选出的错误日志行数|
|`created_at`|DATETIME|归档时间|

### 6.2 向量库 Collection: `log_embeddings`

- `id`: 对应 `log_records.id`
- `embedding`: 摘要的向量数据
- `metadata`: 包含 `package_name`, `summary`, `error_count`

## 7. AI 提示词策略 (Prompt Strategy)

**System Prompt:**

```text
你是一名鸿蒙系统应用开发专家。请分析以下筛选出的 Hilog 错误日志片段。
背景：这些日志已经过预处理，仅包含特定包名的 Error 级别日志，不包含堆栈信息。
任务：
1. 归纳主要错误类型（如：网络错误、权限错误、数据解析错误等）。
2. 提取出现频率最高的 errorCode 和 errorMessage。
3. 推测可能的业务原因。
4. 生成一个简短的文件夹命名建议（格式：YYYYMMDD_包名_核心问题，不含特殊字符）。

日志片段：
{filtered_logs}
```

## 8. 开发阶段规划 (MVP Roadmap)

- **Phase 1 (文件解析核心)**：实现 ZIP 递归查找 `hilog` 文件夹，实现流式读取 txt 并按正则筛选 `E` 级别和关键字。**（这是最难也是最基础的部分）**
- **Phase 2 (GUI 与归档)**：完成 CustomTkinter 界面，实现文件拖拽、包名输入、归档移动逻辑。
- **Phase 3 (AI 集成)**：接入 Ollama，实现筛选后日志的发送与摘要生成。
- **Phase 4 (检索)**：实现 SQLite 查询和 ChromaDB 语义搜索。