import logging
import logging.config

from src.core.logger import LOGGING


def get_logger(name: str = __name__):
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(name)
