from email_summarizer.app.utils.exchange_client import ExchangeClient
from email_summarizer.app.agents.graph.email_summarizer_graph import EmailSummarizerAgentsGraph
import datetime

if __name__ == "__main__":
    client = ExchangeClient()
    emails = client.fetch_all_emails()
    email_summarization_date = datetime.date.today().strftime("%Y-%m-%d")
    agents = EmailSummarizerAgentsGraph(selected_analysts=["briefing_analyst", "status_updates"])

    final_state = agents.propagate(emails, email_summarization_date)

    print("=== Final State ===")
    print(final_state["email_summary_report"])
