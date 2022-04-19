from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

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
        return roles, HTTPStatus.OK

    @use_kwargs(RoleSchema)
    @marshal_with(RoleSchema)
    def post(self, **kwargs):
        """Создать новую роль"""
        role = role_access.create(**kwargs)

        return role, HTTPStatus.CREATED


@doc(tags=[tag])
class Role(MethodResource, Resource):
    """Получить, удалить, изменить роль по uuid"""

    @marshal_with(RoleSchema)
    def get(self, uuid: UUID):
        """Получить роль по uuid"""
        role = role_access.get_by_id(uuid)
        return role, HTTPStatus.OK

    @use_kwargs(RoleSchema)
    @marshal_with(RoleSchema)
    def put(self, uuid: UUID, **kwargs):
        """Изменение роли"""
        role = role_access.update(uuid, **kwargs)
        return role, HTTPStatus.OK

    def delete(self, uuid: UUID):
        """Удаление роли"""
        role_access.delete(uuid)
        return {'message': 'Role is deleted'}, HTTPStatus.OK
