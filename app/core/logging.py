import logging, sys
from loguru import logger

class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except Exception:
            level = record.levelno
        logger.bind(module=record.module).log(level, record.getMessage())

def setup_logging():
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)
    logger.remove()
    logger.add(sys.stdout, enqueue=True, backtrace=False, diagnose=False)