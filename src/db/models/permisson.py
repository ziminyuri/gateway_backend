from src.db import db
from src.db.models.base import PrimaryModel


class Permission(PrimaryModel):
    __tablename__ = 'permission'

    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Permission {self.name}>'
