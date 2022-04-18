from http import HTTPStatus

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restx import Resource

from api.v1.serializers.roles import RoleSchema
from db.access import RoleAccess

role_access = RoleAccess()
tag = 'Role'


@doc(tags=[tag])
class Roles(MethodResource, Resource):
    """Показать список всех ролей или создать новую роль"""

    @marshal_with(RoleSchema(many=True))
    def get(self):
        """Получить список всех ролей"""
        roles = role_access.get_all()
        return roles

    @use_kwargs(RoleSchema)
    @marshal_with(RoleSchema)
    def post(self, **kwargs):
        """Создать новую роль"""
        role = role_access.create(**kwargs)

        return role, HTTPStatus.CREATED


@doc(tags=[tag])
class Role(MethodResource, Resource):
    """Получить, удалить, изменить роль по uuid"""

    def get(self, uuid):
        """Получить список всех ролей"""
        return {'message': 'My First Awesome API'}
