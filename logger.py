import logging
import os
from datetime import datetime

def setup_logger():
    """Sets up a logger for the application, creating a new log file for each run based on the current timestamp."""
    
    # Directory to store log files
    log_dir = './logs'
    
    # Ensure the log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create a unique log filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # e.g., 2024-10-07_14-35-22
    log_file = f'app_{timestamp}.log'
    log_path = os.path.join(log_dir, log_file)

    # Configure logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create handlers for file and console logging
    file_handler = logging.FileHandler(log_path)
    console_handler = logging.StreamHandler()

    # Set log level for both handlers
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info(f"Logger initialized. Logs will be saved to: {log_path}")
    
    return logger

logger = setup_logger()
