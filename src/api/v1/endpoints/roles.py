from http import HTTPStatus

from flask import request
from flask_restx import Resource

from api.v1.endpoints import role_ns
from api.v1.serializers.roles import RoleSchema, role_model
from db.access import RoleAccess

role_schema = RoleSchema()
role_access = RoleAccess()


@role_ns.route('/')
class Roles(Resource):
    """Показать список всех ролей или создать новую роль"""

    @role_ns.response(HTTPStatus.OK, 'Roles are issued')
    @role_ns.marshal_list_with(role_model)
    def get(self):
        """Получить список всех ролей"""
        roles = role_access.get_all()
        return roles

    @role_ns.expect(role_model, validate=True)
    @role_ns.response(HTTPStatus.CREATED, 'Role was created')
    @role_ns.marshal_with(role_model, code=HTTPStatus.CREATED)
    def post(self):
        """Создать новую роль"""
        data = request.json

        errors = role_schema.validate(data)
        if errors:
            return str(errors), HTTPStatus.BAD_REQUEST

        role = role_access.create(**data)
        return role


@role_ns.route('/<int:uuid>')
@role_ns.response(HTTPStatus.NOT_FOUND, 'Role not found')
@role_ns.param('uuid', 'Role identifier')
class Role(Resource):
    """Получить, удалить, изменить роль по uuid"""
    pass
