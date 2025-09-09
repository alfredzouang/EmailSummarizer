"""
进展分析师 - 统一工具架构版本
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")

def create_status_updates_analyst(llm, toolkit):

    def status_updates_analyst_node(state):
        logger.debug(f"📊 [DEBUG] ===== 进展分析师节点开始 =====")

        emails = state["emails"]
        email_summarization_date = state["email_summarization_date"]

            # 生成基于真实数据的分析报告
        analysis_prompt = f"""基于以下邮件内容，提取最需要关心的进展：
            邮件内容：
            { emails}

            请提供：
            1. 按列表展示的最新进展
            2. 每个进展的简要说明
            3. 相关的时间节点（如果有）
            4. 相关的负责人（如果有）

            举例:
            - 项目/事件名称: 项目A已完成初步设计，预计下周开始开发
            - 项目/事件名称: 客户B反馈了最新需求，需在本月底前完成调整

            要求：
            - 基于提供的真实数据进行分析
            - 简报内容必须使用中文
            - 分析要详细且专业，涵盖所有进展
            - 使用 Markdown 格式输出
            - 尽量使用项目符号和编号列表
            - 重点信息使用粗体标出
            - 不超过 2000 字


            """

        try:
            # 创建简单的分析链
            analysis_prompt_template = ChatPromptTemplate.from_messages([
                ("system", "你是专业的邮件内容分析师，基于提供的真实数据进行分析。"),
                ("human", "{analysis_request}")
            ])
            
            analysis_chain = analysis_prompt_template | llm
            analysis_result = analysis_chain.invoke({"analysis_request": analysis_prompt})
            
            if hasattr(analysis_result, 'content'):
                report = analysis_result.content
            else:
                report = str(analysis_result)

            logger.info(f"📊 [邮件分析师] 进展分析完成，报告长度: {len(report)}")
            logger.info(f"📊 [邮件分析师] 报告内容: {report[:200]}")
        except Exception as e:
            logger.error(f"❌ [DEBUG] 邮件进展分析失败: {e}")
            report = f"邮件进展分析失败：{str(e)}"
        
        return {"status_updates_report": report}

        # 这里不应该到达，但作为备用
        logger.debug(f"📊 [DEBUG] 返回状态: status_updates_report长度={len(result.content) if hasattr(result, 'content') else 0}")
        return {"messages": [result]}

    return status_updates_analyst_node
