from uuid import UUID

from src.db.access import PermissionAccess
from src.db.access.base import DatabaseAccess
from src.db.models import Role


class RoleAccess(DatabaseAccess):
    """Класс доступа к базе данных для ролей"""

    def __init__(self):
        self.permission_access = PermissionAccess()
        super().__init__(Role)

    def get_all_permissions(self, id_: UUID):
        """Получить все привилегии связанные с ролью"""
        role = self.get_by_id(id_)
        return role.permissions

    def add_permission(self, role_id: UUID, permission_id: UUID):
        """Добавить привилегию к роли"""
        permission, role = self._get_permission_role(permission_id, role_id)
        role.permissions.append(permission)
        self.commit()

    def remove_permission(self, role_id: UUID, permission_id: UUID):
        """Удалить привилегию из роли"""
        permission, role = self._get_permission_role(permission_id, role_id)
        role.permissions.remove(permission)
        self.commit()

    def _get_permission_role(self, permission_id: UUID, role_id: UUID):
        """Получить роли и привилегию по uuid"""
        role = self.get_by_id(role_id)
        permission = self.permission_access.get_by_id(permission_id)
        return permission, role
