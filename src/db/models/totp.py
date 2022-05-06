from sqlalchemy.dialects.postgresql import UUID

from src.db import db
from src.db.models.base import PrimaryIdModel


class Totp(PrimaryIdModel):
    __tablename__ = 'totp'

    secret = db.Column(db.String, nullable=False, unique=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)
