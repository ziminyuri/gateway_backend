from db.models.base import PrimaryModel
from db.models.connect_tables import permission_role_table
from db.models.database import db


class Role(PrimaryModel):
    __tablename__ = 'role'

    name = db.Column(db.String, nullable=False, unique=True)
    permissions = db.relationship('Permission', secondary=permission_role_table,
                                  backref='roles', lazy=True)

    def __repr__(self):
        return f'<Role {self.name}>'
