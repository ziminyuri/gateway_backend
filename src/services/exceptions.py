class DatabaseExceptions(Exception):
    """Класс ошибок базы данных"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UserException(Exception):
    """Класс ошибки для юзера"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class TokenException(Exception):
    """Класс ошибки для токенов"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)
