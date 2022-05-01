import logging
import logging.config

from flask_restful import reqparse

from src.core.logger import LOGGING


def get_logger(name: str = __name__):
    logging.config.dictConfig(LOGGING)
    return logging.getLogger(name)


def get_pagination_params():
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, help='Page for pagination')
    parser.add_argument('number', type=int, help='Number of items for pagination')
    return parser.parse_args()
