from http import HTTPStatus

from flask import Flask
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from services.exceptions import DatabaseExceptions


def handle_db_exception(error):
    """Возвращает ошибки базы данных"""
    message = f"Database exception: {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST


def no_db_result_found(error):
    """Возвращает ошибку если нет записи в базе данных"""
    message = f"Database result not found. {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST


def validation_exception(error):
    """Возвращает ошибку если не прошла валидация"""
    if isinstance(error.exc, ValidationError):
        return {'message': error.data['messages']['json']}, \
               HTTPStatus.BAD_REQUEST

    return error, HTTPStatus.UNPROCESSABLE_ENTITY


def register_errors(app: Flask):
    app.register_error_handler(
        DatabaseExceptions, handle_db_exception)
    app.register_error_handler(
        NoResultFound, no_db_result_found)
    app.register_error_handler(
        HTTPStatus.UNPROCESSABLE_ENTITY, validation_exception)
