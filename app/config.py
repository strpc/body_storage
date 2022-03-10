from enum import Enum

from pydantic import BaseSettings


class LogLevelEnum(str, Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class AppConfig(BaseSettings):
    LOG_LEVEL: LogLevelEnum = LogLevelEnum.INFO


def get_config() -> AppConfig:
    return AppConfig()
