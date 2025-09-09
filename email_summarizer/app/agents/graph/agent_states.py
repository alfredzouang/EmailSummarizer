from typing import Annotated, Sequence
from datetime import date, timedelta, datetime
from typing_extensions import TypedDict, Optional
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph, START, MessagesState

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")


# Status updates team state
class StatusUpdatesState(TypedDict):
    history: Annotated[str, "Conversation history"]  # Conversation history
    current_response: Annotated[str, "Latest response"]  # Last response
    judge_decision: Annotated[str, "Final judge decision"]  # Last response
    count: Annotated[int, "Length of the current conversation"]  # Conversation length


# Action items team state
class ActionItemsState(TypedDict):
    history: Annotated[str, "Conversation history"]  # Conversation history
    latest_speaker: Annotated[str, "Analyst that spoke last"]
    current_response: Annotated[
        str, "Latest response by the risky analyst"
    ]  # Last response
    judge_decision: Annotated[str, "Judge's decision"]
    count: Annotated[int, "Length of the current conversation"]  # Conversation length

class AgentState(MessagesState):
    """State for the email summarization agents."""
    emails: Annotated[dict, "Emails to be summarized"]
    email_summarization_date: Annotated[str, "What date are we summarizing emails for"]

    sender: Annotated[str, "Agent that sent this message"]

    # research step
    briefing_report: Annotated[str, "Report from the Briefing Analyst"]
    status_updates_report: Annotated[str, "Report from the Status Updates Analyst"]
    action_items_report: Annotated[
        str, "Report from the Action Items Researcher"
    ]

    # status updates team discussion step
    status_updates_state: Annotated[
        StatusUpdatesState, "Current state of the status updates discussion"
    ]

    # action items team discussion step
    action_items_state: Annotated[
        ActionItemsState, "Current state of the action items discussion"
    ]

    email_summary_report: Annotated[str, "Final email summary report"]
