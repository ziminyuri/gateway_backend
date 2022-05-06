from uuid import UUID

from sqlalchemy.orm.exc import NoResultFound

from src.db.access import RoleAccess
from src.db.access.base import DatabaseAccess
from src.db.models import User


class UserAccess(DatabaseAccess):
    """ Класс доступа к базе данных для пользователей """

    def __init__(self):
        self.role_access = RoleAccess()
        super().__init__(User)

    @staticmethod
    def get_by_username(username):
        user = User.lookup(username)
        if not user:
            raise NoResultFound(f"No record with username: {username}")

        return user

    @staticmethod
    def get_by_username_or_none(username):
        return User.lookup(username)

    def get_all_roles(self, id_: UUID):
        """Получить все роли пользователя"""
        user = self.get_by_id(id_)
        return user.roles

    def assign_role(self, user_id: UUID, role_id: UUID):
        """Назначить пользователю роль"""
        user, role = self._get_user_role(user_id, role_id)
        user.roles.append(role)
        self.commit()

    def remove_role(self, user_id: UUID, role_id: UUID):
        """Удалить роль у пользователя"""
        user, role = self._get_user_role(user_id, role_id)
        user.roles.remove(role)
        self.commit()

    def _get_user_role(self, user_id: UUID, role_id: UUID):
        """Получить пользователя и роль по uuid"""
        user = self.get_by_id(user_id)
        role = self.role_access.get_by_id(role_id)
        return user, role
