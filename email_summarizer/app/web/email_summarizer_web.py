import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import streamlit as st
import datetime
from email_summarizer.app.utils.exchange_client import ExchangeClient
from email_summarizer.app.agents.graph.email_summarizer_graph import EmailSummarizerAgentsGraph

st.set_page_config(layout="wide")
st.title("Email Summarizer Demo")

# Sidebar: Fetch and display today's emails
st.sidebar.header("Email List")

if "emails" not in st.session_state:
    st.session_state["emails"] = []

def fetch_emails():
    client = ExchangeClient()
    emails = client.fetch_all_emails()
    st.session_state["emails"] = emails

if st.sidebar.button("Fetch Today's Emails"):
    fetch_emails()

emails = st.session_state.get("emails", [])

if emails:
    for idx, email in enumerate(emails):
        st.sidebar.markdown(f"**{idx+1}. {email.get('subject', 'No Subject')}**")
        st.sidebar.caption(f"From: {email.get('sender', '')}")
        st.sidebar.caption(f"Received: {email.get('datetime_received', '')}")
        st.sidebar.markdown("---")
        st.sidebar.markdown(email.get("main_content", "")[:200] + "...")
else:
    st.sidebar.info("No emails loaded. Click the button above to fetch today's emails.")

# Main area: Summarize emails
st.header("Email Summary Report")

if "summary_report" not in st.session_state:
    st.session_state["summary_report"] = ""

def summarize_emails():
    if not emails:
        st.warning("No emails to summarize. Please fetch emails first.")
        return
    email_summarization_date = datetime.date.today().strftime("%Y-%m-%d")
    agents = EmailSummarizerAgentsGraph(selected_analysts=["briefing_analyst", "status_updates"])
    final_state = agents.propagate(emails, email_summarization_date)
    st.session_state["summary_report"] = final_state.get("email_summary_report", "")

if st.button("Summarize Emails"):
    summarize_emails()

if st.session_state.get("summary_report", ""):
    st.markdown(st.session_state["summary_report"], unsafe_allow_html=True)
else:
    st.info("Click 'Summarize Emails' to generate a summary report.")
