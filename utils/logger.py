"""
Logging Configuration for Zootekni Pro
"""

import logging
import os
from pathlib import Path
from utils.constants import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT, APP_NAME

def setup_logger(name: str = None) -> logging.Logger:
    """
    Setup application logger.
    
    Args:
        name: Logger name (defaults to APP_NAME)
    
    Returns:
        Logger instance
    """
    logger_name = name or APP_NAME
    
    # Get or create logger
    logger = logging.getLogger(logger_name)
    
    # Don't add handlers if already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # File handler
    log_path = Path(LOG_FILE)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        f"{APP_NAME}: %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str = None) -> logging.Logger:
    """Get existing logger or create new one."""
    return logging.getLogger(name or APP_NAME)