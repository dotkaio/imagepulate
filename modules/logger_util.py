"""Logger utility module for Imagepulate."""

import logging
import sys


def get_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (defaults to module name)
        level: Logging level (defaults to INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)

        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
