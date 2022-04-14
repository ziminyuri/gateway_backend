from db import db
from db.models import PrimaryModel


class Permission(PrimaryModel):
    __tablename__ = 'permission'

    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Permission {self.name}>'
