from db.access.base import DatabaseAccess
from db.models import User


class UserAccess(DatabaseAccess):
    """ Класс доступа к базе данных для пользователей """

    def __init__(self):
        super().__init__(User)
