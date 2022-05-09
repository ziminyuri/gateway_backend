from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from src.db import db
from src.db.models.base import PrimaryUuidModel


# def create_partition_history(target, connection, **kw) -> None:
#     """ Парцеляция таблицы AuthHistory """
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "user_sign_in_smart" PARTITION OF "auth_history" FOR VALUES IN ('smart')"""
#     )
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "user_sign_in_mobile" PARTITION OF "auth_history" FOR VALUES IN ('mobile')"""
#     )
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "user_sign_in_web" PARTITION OF "auth_history" FOR VALUES IN ('web')"""
#     )
#     connection.execute(
#         """CREATE TABLE IF NOT EXISTS "user_sign_in_web"
#          PARTITION OF "auth_history" FOR VALUES NOT IN ('smart') AND
#                                          VALUES NOT IN ('mobile') AND
#                                          VALUES NOT IN ('web')"""
#     )


class AuthHistory(PrimaryUuidModel):
    __tablename__ = 'auth_history'

    login_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_agent = db.Column(db.String, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='history')

    device = db.Column(db.Text)
    ip_address = db.Column(db.String)
