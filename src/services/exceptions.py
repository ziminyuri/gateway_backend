class DatabaseExceptions(Exception):
    """Класс ошибок базы данных"""
    def __init__(self, message):
        self.message = message
        super().__init__(message)
