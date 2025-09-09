from email_summarizer.app.utils.logging_init import get_logger, setup_logging

def main():
    setup_logging()
    logger = get_logger("emailsummarizer")
    logger.info("Logger initialized and working for email_summarizer.")

if __name__ == "__main__":
    main()
