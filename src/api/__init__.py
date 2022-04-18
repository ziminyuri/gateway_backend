from http import HTTPStatus

from flask import Blueprint
from flask_restx import Api

from api.v1.endpoints.roles import role_ns
from services.exceptions import DatabaseExceptions

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint, doc='/doc', title='Auth service')

api.add_namespace(role_ns)


@api.errorhandler(DatabaseExceptions)
def handle_db_exception(error):
    """Возвращает ошибки базы данных"""
    message = f"Database exception: {error}"
    return {'message': message}, HTTPStatus.BAD_REQUEST
