#!/bin/bash
# Start celery worker for email_summarizer

celery -A app.celery_app.celery_app worker --loglevel=info
