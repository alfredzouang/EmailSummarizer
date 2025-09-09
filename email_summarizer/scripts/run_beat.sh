#!/bin/bash
# Start celery beat for email_summarizer

celery -A app.celery_app.celery_app beat --loglevel=info
