from typing import Optional

from fastapi import FastAPI
from loguru import logger

from app.config import AppConfig, LogLevelEnum, get_config
from app.logger import init_logger
from app.transport.http.handlers.body_saver import controllers as body_saver
from app.transport.http.handlers.service import controllers as service


class HTTPApp:
    def __init__(self, app: FastAPI):
        self.app = app

    @classmethod
    def create_app(cls, config: Optional[AppConfig] = None) -> FastAPI:
        app = FastAPI()
        factory = cls(app)

        config = config or get_config()
        factory._init_logger(config.LOG_LEVEL)
        factory._register_routers()
        factory._register_hooks()
        return factory.app

    @staticmethod
    def _init_logger(log_level: LogLevelEnum) -> None:
        init_logger(log_level)

    def _register_routers(self) -> None:
        self.app.include_router(body_saver.router, prefix="/api")
        self.app.include_router(service.router)

    def _register_hooks(self) -> None:
        self._add_startup_hook()
        self._add_shutdown_hook()

    def _add_startup_hook(self) -> None:
        self.app.add_event_handler("startup", self._init_storage)

    def _add_shutdown_hook(self) -> None:
        self.app.add_event_handler("shutdown", self._clear_storage)

    def _init_storage(self) -> None:
        self.app.state.storage = {}
        logger.info("storage inited")

    def _clear_storage(self) -> None:
        del self.app.state.storage
        logger.info("storage cleaned")
