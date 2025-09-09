# Email Summarizer

基于大语言模型（LLM）的邮件自动摘要系统。支持通过 Web 界面一键抓取、分析和总结 Exchange 邮箱中的邮件，适用于高效信息提取和团队协作场景。

## 主要特性

- **多智能体协作**：采用多智能体（Multi-Agent）和图结构（Graph）驱动的邮件分析与摘要流程。
- **可扩展分析师体系**：内置多种分析师（Analyst），支持自定义扩展。
- **Streamlit Web 界面**：一键抓取邮件、生成摘要报告，交互友好。
- **支持 Exchange 邮箱**：通过 exchangelib 集成 Exchange 邮箱数据源。

## 目录结构

```
email_summarizer/
├── app/
│   ├── agents/                # 智能体体系核心
│   │   ├── analysts/          # 各类分析师（如简报、状态、行动项）
│   │   ├── graph/             # 智能体图结构、状态、传播、条件逻辑
│   │   ├── manager/           # 智能体管理器
│   │   ├── agent_utils.py     # 智能体工具函数
│   │   └── multiagent.py      # 多智能体入口
│   ├── tasks/                 # 邮件抓取、摘要等任务
│   ├── utils/                 # 工具与 Exchange 客户端
│   └── web/                   # Web 入口（Streamlit）
├── scripts/                   # 测试与运行脚本
├── README.md
├── pyproject.toml
└── ...
```

## agents 体系说明

- `analysts/`：定义不同分析师（如 briefing_analyst、status_update_analyst、action_items_analyst），每个分析师聚焦不同邮件内容维度。
- `graph/`：核心为 `EmailSummarizerAgentsGraph`，负责智能体间的信息流转、状态管理、条件控制等。
- `manager/`：如 `email_summary_manager.py`，用于统一调度和管理摘要流程。
- `multiagent.py`：多智能体摘要主入口，支持批量邮件摘要。
- `agent_utils.py`：通用工具函数。

## Web 入口

主入口为 `email_summarizer/app/web/email_summarizer_web.py`，基于 Streamlit 实现，支持：

- 侧边栏一键抓取 Exchange 邮箱当天邮件
- 主界面生成并展示邮件摘要报告
- 支持多分析师协作，自动调用 agents 层核心逻辑

## 安装与运行

### 环境要求

- Python >= 3.10

### 安装依赖

```bash
pip install -r requirements.txt
# 或使用 pyproject.toml 支持的工具（如 poetry、pip）
```

### 启动 Web 界面

```bash
streamlit run email_summarizer/app/web/email_summarizer_web.py
```

### 邮箱配置

请在 `email_summarizer/.env` 中配置 Exchange 邮箱相关环境变量，参考 exchangelib 官方文档。

## 依赖

- streamlit
- exchangelib
- celery
- langchain-openai
- langgraph
- openai
- python-dotenv
- 及其他见 pyproject.toml

## 开发与测试

- 主要逻辑单元可通过 `scripts/` 目录下测试脚本进行验证。
- 推荐使用 VSCode 或 PyCharm 进行开发。

## 致谢

本项目受 LangGraph、LangChain 等开源项目启发。
