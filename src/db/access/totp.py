from uuid import UUID

from src.db.access.base import DatabaseAccess
from src.db.models import Totp
from src.services.exceptions import DatabaseExceptions


class TotpAccess(DatabaseAccess):
    """Класс доступа к базе данных для двухфакторной аутентификации """

    def __init__(self):
        super().__init__(Totp)

    def get_by_user_id(self, user_id: UUID):
        record = self.model.query.filter_by(user_id=user_id).first()
        return record.secret

    def create(self, **kwargs):
        try:
            record = super().create(**kwargs)
            return record.secret
        except DatabaseExceptions:
            return self.get_by_user_id(kwargs['user_id'])
