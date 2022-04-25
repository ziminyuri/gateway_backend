from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from src.db import db
from src.db.models.base import PrimaryModel


class AuthHistory(PrimaryModel):
    __tablename__ = 'auth_history'

    login_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_agent = db.Column(db.String, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='history')
