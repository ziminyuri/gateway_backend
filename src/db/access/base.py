from abc import ABC
from typing import List, Optional

from db.models.database import db
from services.exceptions import DatabaseExceptions
from utils import get_logger


class DatabaseAccess(ABC):
    """Абстрактный класс для уровня доступа к базе данных"""

    def __init__(self, model: db.Model):
        self.model = model
        self.session = db.session
        self.logger = get_logger(self.__class__.__name__)

    def get_by_id(self, id_: int) -> db.Model:
        """Получить запись из базы данных по id"""
        entity = self.model.query.filter_by(id=id_).first()
        return entity

    def get_all(self, filters: Optional[dict] = None) -> List[db.Model]:
        """Получаем все записи из базы данных с возможным фильтром"""
        entities = self.model.query
        if filters:
            entities = entities.filter_by(**filters)
        return entities.all()

    def create(self, **kwargs):
        """Создание новой сущности"""
        entity = self.model(**kwargs)
        self._commit(entity)
        return entity

    def _commit(self, entity: db.Model):
        """Создание сущности в базе данных или откат"""
        self.session.add(entity)
        try:
            self.session.commit()
        except Exception as error:
            self.logger.error(
                f"Error: {error} while committing {self.model}"
            )
            self.session.rollback()
            raise DatabaseExceptions(
                f"Во время создания модели: {self.model}"
                f"возникла ошибка: {error}")
