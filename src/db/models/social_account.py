from sqlalchemy.dialects.postgresql import UUID

from src.db import db
from src.db.models.base import AuditModel


class SocialAccount(AuditModel):
    __tablename__ = 'social_account'

    id = db.Column(db.String, nullable=False, primary_key=True)
    social_name = db.Column(db.String, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)

    @classmethod
    def lookup(cls, id, social_name):
        return cls.query.filter_by(id=id, social_name=social_name).one_or_none()
