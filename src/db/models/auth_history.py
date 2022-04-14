from sqlalchemy.sql.functions import func

from db import db
from db.models import PrimaryModel


class AuthHistory(PrimaryModel):
    __tablename__ = 'auth_history'

    login_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_agent = db.Column(db.String, nullable=False)
