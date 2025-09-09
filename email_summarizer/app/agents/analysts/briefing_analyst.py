"""
简报分析师 - 统一工具架构版本
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")

def create_briefing_analyst(llm, toolkit):

    def briefing_analyst_node(state):
        logger.debug(f"📊 [DEBUG] ===== 简报分析师节点开始 =====")

        emails = state["emails"]
        email_summarization_date = state["email_summarization_date"]

        # 统一的系统提示，适用于所有股票类型
        system_message = (
            f"你是一位专业的邮件总结分析师。"
            f"⚠️ 绝对强制要求：你必须使用所提供的真实数据！不允许任何假设或编造！"
            f"任务：分析邮件内容并生成简报。"
            "📊 分析要求："
            "- 基于真实邮件内容进行总结"
            "🌍 语言要求："
            "- 所有分析内容必须使用中文"
            "🚫 严格禁止："
            "- 不允许说'我将调用工具'"
            "- 不允许假设任何数据"
            "- 不允许编造任何信息"
            "✅ 你必须："
            "- 基于真实数据进行分析"
            "- 使用中文输出简报"
            "直接回复简报内容，不要说任何其他话！"
        )

            # 生成基于真实数据的分析报告
        analysis_prompt = f"""基于以下真实数据，对下面的邮件内容进行总结：
            邮件内容：
            { emails}

            请提供：
            1. 邮件内容总结
            2. 邮件重要性评估

            要求：
            - 基于提供的真实数据进行分析
            - 简报内容必须使用中文
            - 分析要详细且专业，涵盖所有关键点
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

            logger.info(f"📊 [邮件分析师] 简报完成，报告长度: {len(report)}")
            logger.info(f"📊 [邮件分析师] 报告内容: {report[:200]}")
        except Exception as e:
            logger.error(f"❌ [DEBUG] 邮件简报分析失败: {e}")
            report = f"邮件简报失败：{str(e)}"
        
        return {"briefing_report": report}

        # 这里不应该到达，但作为备用
        logger.debug(f"📊 [DEBUG] 返回状态: briefing_report长度={len(result.content) if hasattr(result, 'content') else 0}")
        return {"messages": [result]}

    return briefing_analyst_node
