"""
进展分析师 - 统一工具架构版本
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")

def create_action_items_analyst(llm, toolkit):

    def action_items_analyst_node(state):
        logger.debug(f"📊 [DEBUG] ===== 行动项分析师节点开始 =====")

        emails = state["emails"]
        email_summarization_date = state["email_summarization_date"]

            # 生成基于真实数据的分析报告
        analysis_prompt = f"""基于以下邮件内容，提取最需要关注的行动项：
            邮件内容：
            { emails}

            请提供：
            1. 按列表展示的最新行动项
            2. 每个行动项的简要说明
            3. 相关的时间节点
            4. 相关的负责人（如果有）

            举例:
            - 待办事项/任务名称: 完成项目A的初步设计，截止日期下周五, 联系人: **张三**
            - 待办事项/任务名称: 回复客户B的最新需求，截止日期本月底, 联系人: **李四**

            要求：
            - 基于提供的真实数据进行分析
            - 简报内容必须使用中文
            - 分析要详细且专业，涵盖所有行动项
            - 使用 Markdown 格式输出
            - 尽量使用项目符号和编号列表
            - 重点信息使用粗体标出
            - 日期使用<font color="blue">yyyy-mm-dd</font>标出, 如: <font color="blue">2023-10-31</font>, 并加粗显示
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

            logger.info(f"📊 [邮件分析师] 行动项分析完成，报告长度: {len(report)}")
            logger.info(f"📊 [邮件分析师] 报告内容: {report[:200]}")
        except Exception as e:
            logger.error(f"❌ [DEBUG] 分析失败: {e}")
            report = f"邮件行动项分析失败：{str(e)}"

        return {"action_items_report": report}

        # 这里不应该到达，但作为备用
        logger.debug(f"📊 [DEBUG] 返回状态: action_items_report长度={len(result.content) if hasattr(result, 'content') else 0}")
        return {"messages": [result]}

    return action_items_analyst_node
