from db.models.base import AuditModel, PrimaryModel
from db.models.connect_tables import user_role_table
from db.models.database import db


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

    @property
    def identity(self):
        return self.id

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

    def is_valid(self):
        return self.is_active

    def __repr__(self):
        return f'<User {self.username}>'
