"""
Logging configuration for the trading bot.

Sets up a logger that writes structured log entries (requests, responses,
and errors) to a log file, while also printing concise info to console.
"""

import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading_bot.log")


def setup_logger(name: str = "trading_bot") -> logging.Logger:
    """Create and return a configured logger instance.

    Logs to both a rotating log file (bot.log) and the console.
    File logs are more verbose (DEBUG) to help with debugging API issues;
    console logs are kept at INFO level to avoid noise.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler - detailed logs for every API request/response/error
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler - only important info shown to the user
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
