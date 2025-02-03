import logging
from datetime import datetime
import os

def setup_logger():
    """Configure and return a logger instance"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create logger
    logger = logging.getLogger('username_changer')
    logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logging

    # Create handlers
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(f'logs/username_change_{timestamp}.log')
    console_handler = logging.StreamHandler()

    # Set levels for handlers
    file_handler.setLevel(logging.DEBUG)  # Log everything to file
    console_handler.setLevel(logging.INFO)  # Only INFO and above to console

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger