import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from src.db import db


def create_partition_history(target, connection, **kw) -> None:
    """ Партицирование таблицы AuthHistory """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_pc" PARTITION OF "auth_history" FOR VALUES IN ('pc')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_mobile" PARTITION OF "auth_history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_tablet" PARTITION OF "auth_history" FOR VALUES IN ('tablet')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "auth_history_other" PARTITION OF "auth_history" FOR VALUES IN ('other')"""
    )


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'
    __table_args__ = (
        UniqueConstraint('id', 'device_type'),
        {
            'postgresql_partition_by': 'LIST (device_type)',
            'listeners': [('after_create', create_partition_history)],
        }
    )
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    login_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_agent = db.Column(db.String, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='history')

    device_type = db.Column(db.String(10), nullable=False, primary_key=True)
    ip_address = db.Column(db.String)
