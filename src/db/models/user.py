from sqlalchemy.dialects.postgresql import UUID

from db import db
from db.models import AuditModel, PrimaryModel

user_history_table = db.Table(
    'user_history',
    db.Column('user_id',
              UUID,
              db.ForeignKey('user.id'),
              primary_key=True),
    db.Column('history_id',
              UUID,
              db.ForeignKey('auth_history.id'),
              primary_key=True)
)


class User(PrimaryModel, AuditModel):
    __tablename__ = 'user'

    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    profile = db.relationship('Profile', back_populates='user',
                              uselist=False, lazy=True)
    history = db.relationship('AuthHistory', secondary=user_history_table,
                              back_populates='users', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
