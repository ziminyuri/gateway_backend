from sqlalchemy.dialects.postgresql import UUID

from db.models.database import db

user_role_table = db.Table(
    'user_role',
    db.Column('user_id',
              UUID,
              db.ForeignKey('user.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True),
    db.Column('role_id',
              UUID,
              db.ForeignKey('role.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True,))

permission_role_table = db.Table(
    'permission_role',
    db.Column('permission_id',
              UUID,
              db.ForeignKey('permission.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True),
    db.Column('role_id',
              UUID,
              db.ForeignKey('role.id',
                            ondelete="CASCADE",
                            onupdate="CASCADE"),
              primary_key=True))
