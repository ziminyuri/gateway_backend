from flask import request

from src.core.config import REQUEST_LIMIT_PER_MINUTE
from src.db.redis import cache
from src.services.auth import get_user_agent
from src.services.exceptions import RateLimitException


def check_rate_limit(func):
    """Проверка лимита запроса на сервер в минуту"""

    def wrapper(*args, **kwargs):
        identifier = request.remote_addr
        if kwargs.get('user_id'):
            identifier = kwargs.get('user_id')

        user_agent = get_user_agent()
        key = f'{identifier}:{user_agent}'
        request_number = cache.add_request_count(key)

        if request_number > REQUEST_LIMIT_PER_MINUTE:
            raise RateLimitException("Exceeded request limit to server")
        return func(*args, **kwargs)

    return wrapper
