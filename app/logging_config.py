import logging
import sys

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelname

        logger.opt(
            depth=6,
            exception=record.exc_info,
        ).bind(module=record.name).log(level, record.getMessage())


def setup_logging() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        colorize=True,
        format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> | '
        '<level>{level: <8}</level> | '
        '<cyan>{extra[module]}</cyan> | '
        '<level>{message}</level>',
        level='INFO',
        enqueue=True,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

