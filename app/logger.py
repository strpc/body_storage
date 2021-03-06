import sys

from loguru import logger

from app.config import LogLevelEnum


def init_logger(log_level: LogLevelEnum) -> None:
    logger.remove()
    logger.add(sys.stdout, level=log_level)
