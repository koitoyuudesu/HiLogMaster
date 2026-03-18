# LogMaster AI

LogMaster AI 是一个专为鸿蒙系统 Hilog 日志文件设计的 Python 桌面工具，提供自动化解压、筛选、分析与归档功能。

## 功能特性

- **智能文件处理**：自动识别 ZIP/RAR/TXT 文件，递归解压查找 hilog 文件夹
- **日志筛选**：流式读取，仅提取 Error 级别且包含目标包名/关键字的日志
- **AI 智能分析**：调用 LLM 生成分析摘要和归档名建议
- **智能归档**：自动创建归档文件夹，生成分析报告
- **索引注册**：支持 SQLite 和 ChromaDB 双重存储
- **语义搜索**：基于向量数据库的智能检索
- **便捷操作**：支持拖放文件和文件选择器两种方式导入日志

## 技术栈

- **GUI 框架**：CustomTkinter >= 5.2.0, tkinterdnd2 >= 0.3.0
- **文件处理**：chardet >= 5.0.0, rarfile >= 4.0
- **LLM 交互**：requests >= 2.31.0
- **向量数据库**：chromadb >= 0.4.0

## 安装步骤

1. 克隆仓库
```bash
git clone <repository-url>
cd LogMaster
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 使用说明

### 启动应用

```bash
python main.py
```

### 基本操作

1. 在输入框中输入目标包名/关键字
2. 选择日志文件（支持两种方式）：
   - 拖拽日志文件（ZIP/RAR/TXT）到拖放区域
   - 点击拖放区域打开文件选择器选择文件
3. 点击 "Process Logs" 按钮开始处理
4. 等待处理完成，查看分析结果

### 配置说明

配置项可在 `config.py` 中修改：

- `OLLAMA_BASE_URL`：Ollama 服务地址
- `LLM_MODEL`：使用的 LLM 模型
- `ARCHIVE_ROOT_DIR`：归档根目录
- `CONTEXT_LINES`：错误日志上下文行数

## 开发指南

### 项目结构

```
LogMaster/
├── src/                 # 源代码
│   ├── gui/            # GUI 模块
│   ├── core/           # 核心业务逻辑
│   ├── ai/             # AI 模块
│   ├── db/             # 数据库模块
│   └── utils/          # 工具模块
├── tests/              # 测试代码
├── data/               # 数据目录
│   ├── logs/           # 原始日志
│   ├── archives/       # 归档文件
│   └── db/             # 数据库文件
├── assets/             # 资源文件
├── config.py           # 配置文件
├── main.py             # 主入口
└── requirements.txt    # 依赖列表
```

### 运行测试

```bash
python -m pytest tests/
```

## 开发阶段

- **Phase 1**：文件解析核心（已完成基础框架）
- **Phase 2**：GUI 与归档
- **Phase 3**：AI 集成
- **Phase 4**：检索功能

## 许可证

Copyright (c) 2026-2026 灵犀

## 贡献

欢迎提交 Issue 和 Pull Request！