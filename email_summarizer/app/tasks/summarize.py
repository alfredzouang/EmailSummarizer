from app.celery_app import celery_app
from app.tasks.fetch_emails import fetch_today_emails_as_dict
from app.agents.multiagent import MultiAgentSummarizer
from app.tasks.report import generate_report
from app.config import Config
from datetime import datetime

@celery_app.task(name="app.tasks.summarize.daily_summary")
def daily_summary():
    """
    Celery task: fetch today's emails, summarize, and generate report.
    """
    emails = fetch_today_emails_as_dict()
    summarizer = MultiAgentSummarizer()
    summary = summarizer.summarize_emails(emails)
    report = generate_report(summary, emails, report_date=datetime.now())
    # TODO: send report via email or save to file
    print(report)
    return report
