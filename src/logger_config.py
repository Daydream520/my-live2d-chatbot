import logging
import sys

# Get the logger for the application.
# Using a specific name avoids conflicts with the root logger or other libraries.
logger = logging.getLogger("MyLive2DChatbot")
logger.setLevel(logging.INFO)

# Check if the logger already has handlers configured.
# This prevents adding duplicate handlers if the module is imported multiple times.
if not logger.handlers:
    # Create a handler to send log records to the console (standard output).
    handler = logging.StreamHandler(sys.stdout)

    # Create a formatter to define the structure of the log messages.
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set the formatter for the handler.
    handler.setFormatter(formatter)

    # Add the handler to the logger.
    logger.addHandler(handler)

# The configured 'logger' instance is now ready to be imported and used
# in other parts of the project.
# Example usage in another file:
# from src.logger_config import logger
# logger.info("This is an info message.")
