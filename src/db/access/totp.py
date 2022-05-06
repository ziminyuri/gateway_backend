from uuid import UUID

from sqlalchemy.orm.exc import NoResultFound

from src.db.access.base import DatabaseAccess
from src.db.models import Totp
from src.services.exceptions import DatabaseExceptions


class TotpAccess(DatabaseAccess):
    """Класс доступа к базе данных для двухфакторной аутентификации """

    def __init__(self):
        super().__init__(Totp)

    def get_by_user_id(self, user_id: UUID, quite=False):
        record = self.model.query.filter_by(user_id=user_id).first()
        if not record and not quite:
            raise NoResultFound("User does not have 2FA")

        return record

    def create(self, **kwargs):
        try:
            record = super().create(**kwargs)
        except DatabaseExceptions:
            record = self.get_by_user_id(kwargs['user_id'])
        finally:
            return record.secret
