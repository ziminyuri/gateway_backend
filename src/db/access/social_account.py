from src.db.access.base import DatabaseAccess
from src.db.models import SocialAccount


class SocialAccountAccess(DatabaseAccess):
    """ Класс доступа к базе данных аккаунтов пользователей из внешних систем """

    def __init__(self):
        super().__init__(SocialAccount)

    @staticmethod
    def get_by_id_and_social_account(id, social_account):
        return SocialAccount.lookup(id, social_account)
