import logging
import sys
from contextvars import ContextVar
from pathlib import Path
from typing import Optional

from loguru import logger

from app.core.config import settings
from app.core.constants import COLORS, LOGURU_LEVEL_MAP

request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="-")

class LoguruLogger:
    """
    Custom logger class for Loguru
    """

    def __init__(
        self,
        app_name: str,
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        max_size: int = 10000000, # 10MB
        retention: int = 10,
        rotation: str = "00:00"
    ):
        self._app_name = app_name
        self._log_level = log_level
        self._log_file = log_file
        self._max_size = max_size
        self._retention = retention
        self._rotation = rotation
        self._setup_logger()

    def _setup_logger(self):
        """
        configure Loguru logger with console and file handler

        :return:
        """
        logger.remove()

        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            f"{COLORS['BLACK_BG']}" "<level> {level: <8}</level> | "
            f"{COLORS['RESET']}"
            "<cyan>{extra[request_id]}</cyan> | "
            "<cyan>{extra[app_name]}</cyan> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )

        logger.add(
            sys.stdout,
            format= log_format,
            level=self._log_level,
            colorize=True,
            enqueue=True,
        )

        if self._log_file:
            log_path = Path(self._log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)


            # size based rotation
            logger.add(
                self._log_file,
                format=log_format,
                level=self._log_level,
                rotation=self._rotation,
                retention=self._retention,
                enqueue=True,
                serialize=True,
                backtrace=True,
                diagnose=True,
                compression="zip",
                encoding="utf-8",
                max_size=self._max_size,
            )

            # time based rotation
            logger.add(
                f"{self._log_file}-{{time:YYYY-MM-DD}}.log",
                format=log_format,
                level=self._log_level,
                rotation=self._rotation,
                retention=self._retention,
                enqueue=True,
                serialize=True,
                backtrace=True,
                diagnose=True,
                compression="zip",
                encoding="utf-8",
            )

        self.logger = logger.bind(
            app_name=self._app_name,
            request_id=request_id_ctx_var.get(),
        )
    def get_logger(self):
        return self.logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        loguru_level = LOGURU_LEVEL_MAP.get(record.levelno, "INFO")

        # Get the log_id from context or provide a default value
        log_id = request_id_ctx_var.get("-")  # Assuming request_id_ctx_var is a ContextVar

        # Find caller from where originated the log message
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Create a logger with the current log_id, but ensure to not create duplicates
        logger_with_id = logger.bind(
                request_id=log_id,
                app_name = settings.APP_NAME
            )

        # Log the message using Loguru
        logger_with_id.opt(depth=depth, exception=record.exc_info).log(loguru_level, record.getMessage())




# Hijack Uvicorn and FastAPI loggers
def hijack_uvicorn_logger():
    """
    Hijack Uvicorn and FastAPI loggers to use Loguru
    """
    # logging.basicConfig(level=logging.INFO)  # Ensure the root logger captures INFO logs
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.trace").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").disabled = True
    logging.getLogger("fastapi").handlers = [InterceptHandler()]


# Create logger instance
logger_instance = LoguruLogger(
    app_name=settings.APP_NAME,
    log_level=settings.LOG_LEVEL,
    log_file=getattr(settings, 'LOG_FILE', None)
)

# Get logger for use in other modules
_logger = logger_instance.get_logger()
