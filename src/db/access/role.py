from db.access.base import DatabaseAccess
from db.models import Role


class RoleAccess(DatabaseAccess):
    """Класс доступа к базе данных для ролей"""

    def __init__(self):
        super().__init__(Role)
