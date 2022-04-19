from werkzeug.security import check_password_hash, generate_password_hash
from api.auth import guard
from db.models.base import AuditModel, PrimaryModel
from db.models.connect_tables import user_role_table
from db.models.database import db
import uuid


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
    refresh_tokens = db.relationship('RefreshToken', back_populates='user')

    def __init__(self, username, password, is_superuser=False):
        self.username = username
        self.hashed_password = self.hash_password(password)
        self.is_superuser = is_superuser

    @staticmethod
    def hash_password(password):
        return guard.hash_password(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def identity(self):
        return str(self.id)

    @property
    def rolenames(self):
        # return [role.name for role in self.roles]
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return f'<User {self.username}>'

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
