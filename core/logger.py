import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    logger = logging.getLogger("Arnab")
    logger.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    file_handler = RotatingFileHandler("logs/bot.log", maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
