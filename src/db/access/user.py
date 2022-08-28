from uuid import UUID

from sqlalchemy.orm.exc import NoResultFound

from src.db.access import RoleAccess
from src.db.access.base import DatabaseAccess
from src.db.models import User, user_role_table


class UserAccess(DatabaseAccess):
    """ Класс доступа к базе данных для пользователей """

    def __init__(self):
        self.role_access = RoleAccess()
        super().__init__(User)

    @staticmethod
    def get_by_username(username, quiet=True):
        user = User.lookup(username)
        if not user and not quiet:
            raise NoResultFound(f"No record with username: {username}")

        return user

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

    def get_all_users(self, role_id=None):
        if role_id:
            entities = self.model.query.join(user_role_table).filter(user_role_table.columns.role_id.in_([params]))
        else:
            entities = self.model.query,
        return entities.all()

    def _get_user_role(self, user_id: UUID, role_id: UUID):
        """Получить пользователя и роль по uuid"""
        user = self.get_by_id(user_id)
        role = self.role_access.get_by_id(role_id)
        return user, role
