from datetime import datetime
from typing import List, Dict, Any

def generate_report(summary: str, emails: List[Dict[str, Any]], report_date: datetime = None) -> str:
    """
    Generate a formatted report from the summary and email metadata.
    """
    report_date = report_date or datetime.now()
    report = f"Email Summary Report - {report_date.strftime('%Y-%m-%d')}\n"
    report += "=" * 40 + "\n"
    report += summary + "\n"
    report += "-" * 40 + "\n"
    report += f"Total emails summarized: {len(emails)}\n"
    return report
