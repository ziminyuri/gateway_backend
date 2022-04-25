from werkzeug.security import check_password_hash, generate_password_hash

from src.db import db
from src.db.models.base import AuditModel, PrimaryModel
from src.db.models.connect_tables import user_role_table
from src.services.exceptions import UserException


class User(PrimaryModel, AuditModel):
    __tablename__ = 'user'

    username = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)

    profile = db.relationship('Profile', back_populates='user',
                              uselist=False, lazy=True)
    roles = db.relationship('Role', secondary=user_role_table,
                            backref='users', lazy=True)
    history = db.relationship('AuthHistory', back_populates='user')

    def __init__(self, username, password, is_superuser=False):
        self.username = username
        self.hashed_password = self.hash_password(password)
        self.is_superuser = is_superuser

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        if not check_password_hash(self.hashed_password, password):
            raise UserException('Wrong credentials')
        return True

    @property
    def identity(self):
        return str(self.id)

    @property
    def rolenames(self):
        return [role.name for role in self.roles]

    @property
    def password(self):
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @classmethod
    def validate_username(cls, username):
        if User.lookup(username):
            raise UserException("Not valid username")

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return f'<User {self.username}>'
