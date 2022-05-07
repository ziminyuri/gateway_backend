class ServerBaseException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class DatabaseExceptions(ServerBaseException):
    """Класс ошибок базы данных"""
    pass


class UserException(ServerBaseException):
    """Класс ошибки для юзера"""
    pass


class TokenException(ServerBaseException):
    """Класс ошибки для токенов"""
    pass


class RateLimitException(ServerBaseException):
    """Класс для большого количества запросов на сервер"""
    pass
