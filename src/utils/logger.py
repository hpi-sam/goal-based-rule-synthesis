import logging
import os
from datetime import datetime

# Ensure logs folder exists
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Create a log file with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"log_{timestamp}.log")

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Avoid duplicate handlers if this file is imported multiple times
if not logger.handlers:
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='a')
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter with timestamps
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def get_logger():
    """Return the configured logger instance."""
    return logger
