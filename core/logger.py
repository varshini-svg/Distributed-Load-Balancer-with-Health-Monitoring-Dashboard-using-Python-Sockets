import logging
import os


# -------------------------------
# Create logs directory if not exists
# -------------------------------
LOG_DIR = "logs"
LOG_FILE = "app.log"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_path = os.path.join(LOG_DIR, LOG_FILE)


# -------------------------------
# Configure Logger
# -------------------------------
def get_logger(name="LoadBalancer"):
    logger = logging.getLogger(name)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # -------------------------------
    # Formatter
    # -------------------------------
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # -------------------------------
    # File Handler
    # -------------------------------
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # -------------------------------
    # Console Handler
    # -------------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger