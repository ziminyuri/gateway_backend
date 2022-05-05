from src.db import db
from src.db.models.base import PrimaryIdModel
from src.db.models.connect_tables import permission_role_table


class Permission(PrimaryIdModel):
    __tablename__ = 'permission'

    name = db.Column(db.String, nullable=False, unique=True)
    roles = db.relationship('Role', back_populates='permissions',
                            lazy='dynamic', secondary=permission_role_table)

    def __repr__(self):
        return f'<Permission {self.name}>'
