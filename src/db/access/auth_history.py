from db.access.base import DatabaseAccess
from db.models import AuthHistory


class AuthHistoryAccess(DatabaseAccess):
    """ Класс доступа к базе данных для ведения истории авторизаций"""

    def __init__(self):
        super().__init__(AuthHistory)

    def get_all_user_auth_for_period(self, user_id, period):
        """ Получить все авторизации пользователя за период """
        return self.get_all(f'user_id = \'{user_id}\' and login_at > \'{period}\'')
