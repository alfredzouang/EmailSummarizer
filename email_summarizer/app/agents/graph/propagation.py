# Email Summarizer/app/agents/graph/propagation.py

from typing import Dict, Any

# 导入统一日志系统
from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger("default")
from email_summarizer.app.agents.graph.agent_states import (
    AgentState,
    ActionItemsState,
    StatusUpdatesState,
)


class Propagator:
    """Handles state initialization and propagation through the graph."""

    def __init__(self, max_recur_limit=100):
        """Initialize with configuration parameters."""
        self.max_recur_limit = max_recur_limit

    def create_initial_state(
        self, emails: dict, email_summarization_date: str
    ) -> Dict[str, Any]:
        """Create the initial state for the agent graph."""
        return {
            "messages": [("human", emails)],
            "emails": emails,
            "email_summarization_date": str(email_summarization_date),
            "status_updates_state": StatusUpdatesState(
                {"history": "", "current_response": "", "count": 0}
            ),
            "action_items_state": ActionItemsState(
                {
                    "history": "",
                    "latest_speaker": "",
                    "current_response": "",
                    "judge_decision": "",
                    "count": 0
                }
            ),
            "briefing_report": "",
            "status_updates_report": "",
            "action_items_report": "",
            "email_summary_report": "",
        }

    def get_graph_args(self) -> Dict[str, Any]:
        """Get arguments for the graph invocation."""
        return {
            "stream_mode": "values",
            "config": {"recursion_limit": self.max_recur_limit},
        }
