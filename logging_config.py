import logging

def setup_logging():
    """
    Configures application-wide logging with timestamp, log level, and logger name.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()]
    )

# Logger instance for use across the app
logger = logging.getLogger("string_analysis_api")
