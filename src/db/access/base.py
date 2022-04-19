from abc import ABC
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm.exc import NoResultFound

from db.models.database import db
from services.exceptions import DatabaseExceptions
from utils import get_logger


class DatabaseAccess(ABC):
    """Абстрактный класс для уровня доступа к базе данных"""

    def __init__(self, model: db.Model):
        self.model = model
        self.session = db.session
        self.logger = get_logger(self.__class__.__name__)

    def get_by_id(self, id_: UUID) -> db.Model:
        """Получить запись из базы данных по id"""
        entity = self.model.query.filter_by(id=id_).first()
        if not entity:
            raise NoResultFound(f"No record with id: {id_}"
                                f" for model: {self.model.__name__}")

        return entity

    def get_all(self, filters: Optional[dict] = None) -> List[db.Model]:
        """Получаем все записи из базы данных с возможным фильтром"""
        entities = self.model.query
        if filters:
            entities = entities.filter_by(**filters)
        return entities.all()

    def update(self, id_: UUID, **kwargs):
        """Обновление сущности"""
        self.model.query.filter_by(id=id_).update(kwargs)
        self.commit()
        return self.model.query.filter_by(id=id_).first()

    def delete(self, id_: UUID):
        self.model.query.filter_by(id=id_).delete()
        self.commit()

    def create(self, **kwargs):
        """Создание новой сущности"""
        entity = self.model(**kwargs)
        self.commit(entity)
        return entity

    def commit(self, entity: Optional[db.Model] = None):
        """Создание сущности в базе данных или откат"""
        if entity:
            self.session.add(entity)
        try:
            self.session.commit()
        except Exception as error:
            self.logger.error(
                f"Error: {error} while committing {self.model.__name__}"
            )
            self.session.rollback()
            raise DatabaseExceptions(
                f"Во время коммита модели: {self.model.__name__} "
                f"возникла ошибка: {error}")
