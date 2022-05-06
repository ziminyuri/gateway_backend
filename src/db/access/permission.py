from src.db.access.base import DatabaseAccess
from src.db.models import Permission, Role


class PermissionAccess(DatabaseAccess):
    """Класс доступа к базе данных для ролей"""

    def __init__(self):
        super().__init__(Permission)

    def get_permissions_by_roles(self, ids: list):
        """Получения всех привилегий для списка ролей"""
        permissions = self.model.query.join(self.model.roles).filter(Role.id.in_(ids)).all()
        return [permission.name for permission in permissions]
