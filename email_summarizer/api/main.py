from fastapi import FastAPI
from email_summarizer.api.routers import email, summary

app = FastAPI(
    title="Email Summarizer API",
    description="API for fetching and summarizing emails",
    version="1.0.0"
)

app.include_router(email.router)
app.include_router(summary.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Email Summarizer API"}