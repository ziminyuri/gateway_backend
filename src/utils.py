import logging
import logging.config

from src.core.logger import LOGGING
from flask_rest_paginate import Pagination


def get_logger(name: str = __name__):
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(name)


pagination = Pagination()


def pagination_init(flask_app, db):
    pagination.init_app(flask_app, db)
