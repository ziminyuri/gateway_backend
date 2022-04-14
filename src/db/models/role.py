from db import db
from db.models import PrimaryModel


class Role(PrimaryModel):
    __tablename__ = 'role'

    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'
