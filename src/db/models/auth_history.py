from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from src.db import db
from src.db.models.base import PrimaryUuidModel
from sqlalchemy import UniqueConstraint


def create_partition_history(target, connection, **kw) -> None:
    """ Парцеляция таблицы AuthHistory """
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
        """CREATE TABLE IF NOT EXISTS "auth_history_other"
         PARTITION OF "auth_history" FOR VALUES NOT IN ('pc') AND
                                         VALUES NOT IN ('mobile') AND
                                         VALUES NOT IN ('tablet')"""
    )


class AuthHistory(PrimaryUuidModel):
    __tablename__ = 'auth_history'
    __table_args__ = (
        UniqueConstraint("id", "device"),
        {
            "postgresql_partition_by": "LIST (device)",
            "listeners": [("after_create", create_partition_history)],
        },
    )

    login_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_agent = db.Column(db.String, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='history')

    device = db.Column(db.Text)
    ip_address = db.Column(db.String)


