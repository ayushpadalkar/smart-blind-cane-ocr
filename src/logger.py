"""
logger.py
---------------------------------------

Central logging module for Blind Cane OCR

Author : Ayush Padalkar
"""

import logging
from pathlib import Path

from src.config import LOG_DIR, LOG_LEVEL


class Logger:

    _logger = None

    @staticmethod
    def get_logger():

        if Logger._logger is not None:
            return Logger._logger

        log_file = Path(LOG_DIR) / "ocr.log"

        logger = logging.getLogger("BlindCaneOCR")

        logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

        if logger.hasHandlers():
            logger.handlers.clear()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        # Console Output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File Output
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        Logger._logger = logger

        return logger


logger = Logger.get_logger()


if __name__ == "__main__":

    logger.info("Logger Initialized Successfully")
    logger.warning("Warning Example")
    logger.error("Error Example")