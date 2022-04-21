from http import HTTPStatus

from flask import Flask
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from services.exceptions import (DatabaseExceptions, TokenException,
                                 UserException)


def handle_db_exception(error):
    """Возвращает ошибки базы данных"""
    message = f"Database exception: {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST


def no_db_result_found(error):
    """Возвращает ошибку если нет записи в базе данных"""
    message = f"Database result not found. {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST


def handle_user_exceptions(error):
    """Возвращает ошибку если юзер не прошел валидацию"""
    message = f"Some error with user. {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST


def handle_token_exceptions(error):
    """Возвращает ошибку если токен не прошел валидацию"""
    message = f"Some error with token. {error}"
    return {'message': message}, HTTPStatus.UNAUTHORIZED


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
    app.register_error_handler(
        UserException, handle_user_exceptions)
    app.register_error_handler(
        TokenException, handle_token_exceptions)
