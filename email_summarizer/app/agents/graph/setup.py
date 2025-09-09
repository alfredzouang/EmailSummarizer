# Email Summarizer/app/agents/graph/setup.py

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode

from email_summarizer.app.agents.graph.agent_states import AgentState

from .conditional_logic import ConditionalLogic
from email_summarizer.app.agents.analysts.briefing_analyst import create_briefing_analyst
from email_summarizer.app.agents.analysts.status_update_analyst import create_status_updates_analyst
from email_summarizer.app.agents.manager.email_summary_manager import create_email_summary_manager
from email_summarizer.app.agents.analysts.action_items_analyst import create_action_items_analyst
from email_summarizer.app.agents.agent_utils import create_msg_delete
# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")


class GraphSetup:
    """Handles the setup and configuration of the agent graph."""

    def __init__(
        self,
        quick_thinking_llm: ChatOpenAI,
        deep_thinking_llm: ChatOpenAI,
        # toolkit: Toolkit,
        tool_nodes: Dict[str, ToolNode],
        conditional_logic: ConditionalLogic,
        config: Dict[str, Any] = None,
        react_llm = None,
    ):
        """Initialize with required components."""
        self.quick_thinking_llm = quick_thinking_llm
        self.deep_thinking_llm = deep_thinking_llm
        self.toolkit = None  # toolkit
        self.tool_nodes = tool_nodes
        self.conditional_logic = conditional_logic
        self.config = config or {}
        self.react_llm = react_llm

    def setup_graph(
        self, selected_analysts=["briefing", "action_items", "status_updates", "fundamentals"]
    ):
        """Set up and compile the agent workflow graph.

        Args:
            selected_analysts (list): List of analyst types to include. Options are:
                - "briefing": Briefing analyst
                - "action_items": Action items analyst
                - "status_updates": Status updates analyst
                - "fundamentals": Fundamentals analyst
        """
        if len(selected_analysts) == 0:
            raise ValueError("Email Summarizer Agents Graph Setup Error: no analysts selected!")

        # Create analyst nodes
        analyst_nodes = {}
        delete_nodes = {}
        tool_nodes = {}

        if "briefing" in selected_analysts:
            # 所有LLM都使用标准分析师
            analyst_nodes["briefing"] = create_briefing_analyst(
                self.quick_thinking_llm, self.toolkit
            )
            delete_nodes["briefing"] = create_msg_delete()
            # tool_nodes["briefing"] = self.tool_nodes["briefing"]

        if "status_updates" in selected_analysts:
            analyst_nodes["status_updates"] = create_status_updates_analyst(
                self.quick_thinking_llm, self.toolkit
            )
            # tool_nodes["status_updates"] = self.tool_nodes["status_updates"]
            delete_nodes["status_updates"] = create_msg_delete()


        email_summary_manager_node = create_email_summary_manager(self.deep_thinking_llm)


        # Create workflow
        workflow = StateGraph(AgentState)

        workflow.add_node("briefing", create_briefing_analyst(
                self.quick_thinking_llm, self.toolkit
            ))
        workflow.add_node("status_updates", create_status_updates_analyst(
                self.quick_thinking_llm, self.toolkit
            ))
        workflow.add_node("action_items", create_action_items_analyst(
                self.quick_thinking_llm, self.toolkit
            ))
        workflow.add_node("clear_action_items", create_msg_delete())
        workflow.add_node("clear_briefing", create_msg_delete())
        workflow.add_node("clear_status_updates", create_msg_delete())
        # Add other nodes
        workflow.add_node("email_summary_manager", email_summary_manager_node)

        workflow.add_edge(START, "briefing")
        workflow.add_edge("briefing", "clear_briefing")
        workflow.add_edge("status_updates", "clear_status_updates")
        workflow.add_edge("clear_briefing", "status_updates")
        workflow.add_edge("clear_status_updates", "action_items")
        workflow.add_edge("action_items", "clear_action_items")
        workflow.add_edge("clear_action_items", "email_summary_manager")
        workflow.add_edge("email_summary_manager", END)

        # Compile and return
        return workflow.compile()
