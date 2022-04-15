from db.models.base import AuditModel, PrimaryModel
from db.models.connect_tables import user_role_table
from db.models.database import db


class User(PrimaryModel, AuditModel):
    __tablename__ = 'user'

    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)

    profile = db.relationship('Profile', back_populates='user',
                              uselist=False, lazy=True)
    roles = db.relationship('Role', secondary=user_role_table,
                            back_populates='users', lazy=True)
    history = db.relationship('AuthHistory', back_populates='user')
    refresh_token = db.relationship('RefreshToken', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'
