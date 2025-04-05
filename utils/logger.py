import sys
import time
from contextlib import contextmanager

from loguru import logger


def setup_logger(log_level: str = "INFO"):
    """
    Configure and set up the logger with console handler only.

    Args:
        log_level: Minimum log level to capture

    Returns:
        The configured logger instance
    """
    # Remove default handlers
    logger.remove()

    # Add console handler with colors
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{file.name}:{function}:{line}</cyan> - "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    return logger


@contextmanager
def log_time(task_name: str, level: str = "INFO"):
    """
    Context manager to log the execution time of a code block.

    Args:
        task_name: Name of the task being timed
        level: Log level to use

    Example:
        with log_time("Data processing"):
            process_data()
    """
    start_time = time.time()
    logger.log(level, f"Starting {task_name}...")
    try:
        yield
    finally:
        elapsed = time.time() - start_time
        logger.log(level, f"Completed {task_name} in {elapsed:.2f} seconds")


logger = setup_logger()  # noqa F811
