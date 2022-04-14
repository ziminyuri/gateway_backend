from sqlalchemy.dialects.postgresql import UUID

from db import db
from db.models import PrimaryModel


class RefreshToken(PrimaryModel):
    __tablename__ = 'refresh_token'

    token = db.Column(db.String, nullable=False, unique=True)
    user_agent = db.Column(db.String, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='refresh_tokens')

    def __repr__(self):
        return f'<RefreshToken {self.token}>'
