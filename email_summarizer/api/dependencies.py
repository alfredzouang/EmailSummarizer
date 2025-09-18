from fastapi import Depends, HTTPException, status

from email_summarizer.app.utils.exchange_client import ExchangeClient
from email_summarizer.app.agents.graph.email_summarizer_graph import EmailSummarizerAgentsGraph
from email_summarizer.app.config import Config

def get_exchange_client(target_email: str):
    """Create and return an ExchangeClient instance."""
    try:
        return ExchangeClient(target_email=target_email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize Exchange client: {str(e)}"
        )

def get_email_summarizer(selected_analysts=None):
    """Create and return an EmailSummarizerAgentsGraph instance."""
    if selected_analysts is None:
        selected_analysts = ["briefing_analyst", "status_updates"]
    
    try:
        return EmailSummarizerAgentsGraph(selected_analysts=selected_analysts)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize EmailSummarizerAgentsGraph: {str(e)}"
        )