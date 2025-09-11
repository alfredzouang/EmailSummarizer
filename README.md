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

本项目使用 [uv](https://github.com/astral-sh/uv) 进行依赖管理，推荐全程使用 uv 操作依赖。

#### 安装 uv（如未安装）

```bash
pip install uv
# 或参考官方文档：https://github.com/astral-sh/uv
```

#### 安装依赖

```bash
uv pip install -r requirements.txt
# 或直接使用 pyproject.toml/uv.lock
uv pip install -r requirements.txt --use-uv
```

#### 常用 uv 命令

- 安装依赖：`uv pip install -r requirements.txt`
- 添加依赖：`uv pip install 包名`
- 移除依赖：`uv pip uninstall 包名`
- 更新锁文件：`uv pip freeze > requirements.txt && uv pip compile`
- 生成/更新 uv.lock：`uv pip compile`

详细用法见 [uv 官方文档](https://github.com/astral-sh/uv)。

### 启动 Web 界面

```bash
streamlit run email_summarizer/app/web/email_summarizer_web.py
```

### 邮箱配置

请根据项目根目录下的 `email_summarizer/.env.example` 文件，复制为 `email_summarizer/.env` 并填写你自己的 Exchange 邮箱、Azure OpenAI、Celery 等相关环境变量。  
**注意：请勿提交包含敏感信息的 .env 文件到版本库。**

各字段说明及示例见 `.env.example`，如需详细配置可参考 [exchangelib 官方文档](https://ecederstrand.github.io/exchangelib/) 及 Azure OpenAI 文档。

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
