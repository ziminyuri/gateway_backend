from sqlalchemy.dialects.postgresql import UUID

from db import db
from db.models import AuditModel, PrimaryModel


class Profile(PrimaryModel, AuditModel):
    __tablename__ = 'profile'

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='profile')

    def __repr__(self):
        return f'<Profile {self.first_name} {self.last_name}>'
