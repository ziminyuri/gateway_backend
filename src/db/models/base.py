import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import func

from db import db


class PrimaryModel(db.Model):
    """Абстрактная модель с primary key"""
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False)


class AuditModel(db.Model):
    """Абстрактная модель для аудита"""
    __abstract__ = True

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now(), nullable=False)
