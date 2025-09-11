# Email Summarizer/app/agents/graph/conditional_logic.py

from email_summarizer.app.agents.graph.agent_states import AgentState

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")


class ConditionalLogic:
    """Handles conditional logic for determining graph flow."""

    def __init__(self, max_debate_rounds=1, max_action_items_rounds=1):
        """Initialize with configuration parameters."""
        self.max_debate_rounds = max_debate_rounds
        self.max_action_items_rounds = max_action_items_rounds

    def should_continue_briefing_analyst(self, state: AgentState):
        """Determine if briefing should continue."""
        messages = state["messages"]
        last_message = messages[-1]

        # 只有AIMessage才有tool_calls属性
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools_briefing"
        return "clear_briefing"

    def should_continue_action_items(self, state: AgentState):
        """Determine if action items analysis should continue."""
        messages = state["messages"]
        last_message = messages[-1]

        # 只有AIMessage才有tool_calls属性
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools_action_items"
        return "Msg Clear Action Items"

    def should_continue_status_updates(self, state: AgentState):
        """Determine if status updates should continue."""
        messages = state["messages"]
        last_message = messages[-1]

        # 只有AIMessage才有tool_calls属性
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools_status_updates"
        return "clear_status_updates"

    def should_continue_debate(self, state: AgentState) -> str:
        """Determine if debate should continue."""

        if (
            state["status_updates_state"]["count"] >= self.max_debate_rounds
        ):  # 3 rounds of back-and-forth between 2 agents
            return "Email Summary Manager"

    def should_continue_action_items(self, state: AgentState) -> str:
        """Determine if action items analysis should continue."""
        if (
            state["action_items_state"]["count"] >= self.max_action_items_rounds
        ):  # 3 rounds of back-and-forth between 3 agents
            return "Action Items Judge"
