import logging.config

from core.config import LoggerSettings


LOGGING_CONFIG = LoggerSettings().dict()
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("my_logger")
