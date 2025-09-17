# Email Summarizer/graph/email_summarizer_graph.py

import os
from pathlib import Path
import json
from datetime import date
from typing import Dict, Any, Tuple, List, Optional

from langchain_openai import ChatOpenAI, AzureChatOpenAI

from langgraph.prebuilt import ToolNode

from email_summarizer.app.utils.logging_init import get_logger
logger = get_logger('agents')
from email_summarizer.app.agents.graph.agent_states import (
    AgentState,
    StatusUpdatesState,
    ActionItemsState,
)

from email_summarizer.app.agents.config.default_config import DEFAULT_CONFIG
from email_summarizer.app.config import Config
from .conditional_logic import ConditionalLogic
from .setup import GraphSetup
from .propagation import Propagator

class EmailSummarizerAgentsGraph:
    """Main class that orchestrates the email summarization agents framework."""

    def __init__(
        self,
        selected_analysts=["briefing", "status_updates"],
        config: Dict[str, Any] = None,
        debug: bool = False,
    ):
        """Initialize the email summarization agents graph and components.

        Args:
            selected_analysts: List of analyst types to include
        """

        if config is None:
            from email_summarizer.app.utils.config_manager import ConfigManager
            config = ConfigManager().get_config()
        self.config = config

        self.debug = debug
        provider = Config.LLM_PROVIDER.lower()
        logger.info(f"🌐 [CONFIG] Using provider: {provider}")

         # Initialize LLMs
        if provider == "azureopenai":
            logger.info("🌐 [CONFIG] Initializing Azure OpenAI LLMs")
            self.deep_thinking_llm = AzureChatOpenAI(
                azure_deployment=self.config.get("deep_think_llm", Config.DEEP_THINK_LLM),
                azure_endpoint=self.config.get("backend_url", Config.BACKEND_URL),
                api_version=self.config.get("api_version", Config.API_VERSION),
                api_key=Config.AZURE_OPENAI_API_KEY
            )
            self.quick_thinking_llm = AzureChatOpenAI(
                azure_deployment=self.config.get("quick_think_llm", Config.QUICK_THINK_LLM),
                azure_endpoint=self.config.get("backend_url", Config.BACKEND_URL),
                api_version=self.config.get("api_version", Config.API_VERSION),
                api_key=Config.AZURE_OPENAI_API_KEY
            )
        elif provider in ("openai", "ollama", "openrouter"):
            logger.info(f"🌐 [CONFIG] Initializing {provider} LLMs")
            self.deep_thinking_llm = ChatOpenAI(
                model_name=self.config.get("deep_think_llm", Config.DEEP_THINK_LLM),
                base_url=self.config.get("backend_url", Config.BACKEND_URL),
                temperature=self.config.get("temperature", Config.TEMPERATURE),
            )
            self.quick_thinking_llm = ChatOpenAI(
                model_name=self.config.get("quick_think_llm", Config.QUICK_THINK_LLM),
                base_url=self.config.get("backend_url", Config.BACKEND_URL),
                temperature=self.config.get("temperature", Config.TEMPERATURE),
            )
            
        # self.toolkit = Toolkit(config=self.config)

        self.tool_nodes = self._create_tool_nodes()

        self.conditional_logic = ConditionalLogic()
        self.graph_setup = GraphSetup(
            self.quick_thinking_llm,
            self.deep_thinking_llm,
            # self.toolkit,
            self.tool_nodes,
            self.conditional_logic,
            self.config,
            getattr(self, 'react_llm', None),
        )

        self.propagator = Propagator()

        self.curr_state = None
        self.ticker = None
        self.log_states_dict = {}

        self.graph = self.graph_setup.setup_graph(selected_analysts)

    def _create_tool_nodes(self) -> Dict[str, ToolNode]:
        return {
            "briefing": ToolNode(
                [
                ]
            ),
            "status_updates": ToolNode(
                [
                ]
            ),
            "action_items": ToolNode(
                [
                ]
            ),
            "fundamentals": ToolNode(
                [
                ]
            ),
        }

    def propagate(self, emails, email_summarization_date):
        logger.debug(f"🔍 [GRAPH DEBUG] ===== EmailSummarizer.propagate 接收参数 =====")
        logger.debug(f"🔍 [GRAPH DEBUG] 接收到的emails: '{emails}' (类型: {type(emails)})")
        logger.debug(f"🔍 [GRAPH DEBUG] 接收到的email_summarization_date: '{email_summarization_date}' (类型: {type(email_summarization_date)})")

        self.emails = emails
        logger.debug(f"🔍 [GRAPH DEBUG] 设置self.emails: '{self.emails}'")

        init_agent_state = self.propagator.create_initial_state(
            emails, email_summarization_date
        )
        args = self.propagator.get_graph_args()

        if self.debug:
            trace = []
            for chunk in self.graph.stream(init_agent_state, **args):
                if len(chunk["messages"]) == 0:
                    pass
                else:
                    chunk["messages"][-1].pretty_print()
                    trace.append(chunk)
            final_state = trace[-1]
        else:
            final_state = self.graph.invoke(init_agent_state, **args)

        self.curr_state = final_state
        return final_state

