from http import HTTPStatus

from flask import Blueprint
from flask_restx import Api

from api.v1.endpoints.roles import Role, Roles
from core.config import BLUEPRINT_API, URL_PREFIX
from services.exceptions import DatabaseExceptions

blueprint = Blueprint(BLUEPRINT_API, __name__, url_prefix=URL_PREFIX)
api = Api(blueprint, doc=False, title='Auth service')

api.add_resource(Roles, '/role')
api.add_resource(Role, '/role/<int:uuid>')


@api.errorhandler(DatabaseExceptions)
def handle_db_exception(error):
    """Возвращает ошибки базы данных"""
    message = f"Database exception: {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST
