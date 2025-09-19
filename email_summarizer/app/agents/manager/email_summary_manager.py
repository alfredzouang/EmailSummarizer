import functools
import time
import json

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")


def create_email_summary_manager(llm, memory=None):
    def email_summary_node(state, name):
        emails = state["emails"]
        email_summarization_date = state["email_summarization_date"]
        status_updates_report = state["status_updates_report"]
        action_items_report = state["action_items_report"]
        briefing_report = state["briefing_report"]

        context = {
            "role": "user",
            "content": f"""
            基于以下三位分析师的报告，生成一份综合的邮件总结报告。
            总计邮件数量: {len(emails) if emails else 0}
            已读邮件数量: {sum(1 for email in emails if email.get('is_read')) if emails else 0}
            未读邮件数量: {sum(1 for email in emails if not email.get('is_read')) if emails else 0}

            1. 邮件摘要报告: {briefing_report}\n
            2. 状态更新分析师报告: {status_updates_report}\n
            3. 行动项分析师报告: {action_items_report}\n
            \n\n
            利用这些报告对邮件进行深入总结。
            """,
        }

        messages = [
            {
                "role": "system",
                "content": f"""您是一位专业的秘书，负责整理邮件的主要内容以及关键进展和工作项。

⚠️ 重要提醒：当前的总结日期是{email_summarization_date}

🔴 严格要求：
- 邮件总结报告必须严格按照邮件列表中的真实数据
- 所有内容必须基于提供的真实数据，不允许假设或编造
- **必须提供完整的邮件总结报告，不允许为空或询问更多信息**

请在您的报告中包含以下关键信息：
1. **邮件统计**: 总邮件数量，已读和未读邮件数量
2. **邮件摘要**: 明确的邮件内容总结
3. **关键进展**: 任何重要的更新或变化
4. **待办事项**: 需要跟进的具体任务或行动项
5. **会议邀请**: 任何相关的会议邀请或日程安排（如果有）

格式要求：
- 禁止使用#标题，允许使用粗体格式区分各部分
- 禁止使用表格形式汇总信息, 允许使用有序列表和无序列表整理信息

特别注意：
- **绝对不允许说"需要更多信息"**
- **不要说"报告结束"或类似的话，只输出报告内容**

请用中文撰写分析内容, 并确保内容详尽且专业, 涵盖所有关键点。使用Markdown格式输出。
""",
            },
            context,
        ]

        result = llm.invoke(messages)

        return {
            "messages": [result],
            "email_summary_report": result.content,
            "sender": name,
        }

    return functools.partial(email_summary_node, name="email_summary_manager")
