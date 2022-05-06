from sqlalchemy.dialects.postgresql import UUID

from src.db import db

user_role_table = db.Table(
    'user_role',
    db.Column('user_id',
              UUID(as_uuid=True),
              db.ForeignKey('user.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True),
    db.Column('role_id',
              db.ForeignKey('role.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True,))

permission_role_table = db.Table(
    'permission_role',
    db.Column('permission_id',
              db.ForeignKey('permission.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True),
    db.Column('role_id',
              db.ForeignKey('role.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True))
