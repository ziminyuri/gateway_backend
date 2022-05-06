from src.db import db
from src.db.models.base import PrimaryIdModel
from src.db.models.connect_tables import permission_role_table


class Role(PrimaryIdModel):
    __tablename__ = 'role'

    name = db.Column(db.String, nullable=False, unique=True)
    permissions = db.relationship('Permission', secondary=permission_role_table,
                                  back_populates='roles', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'
