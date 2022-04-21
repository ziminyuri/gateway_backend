from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from api.v1.serializers.role import RoleSchema, role_args_parse
from db.access import RoleAccess
from services.auth import login_required

role_access = RoleAccess()
tag = 'Role'


@doc(tags=[tag])
class Roles(MethodResource, Resource):
    """Показать список всех ролей или создать новую роль"""

    @marshal_with(RoleSchema(many=True))
    @login_required(superuser=True)
    def get(self, **kwargs):
        """Получить список всех ролей"""
        roles = role_access.get_all()
        return roles, HTTPStatus.OK

    @use_kwargs(RoleSchema)
    @marshal_with(RoleSchema)
    @login_required(superuser=True)
    def post(self, **kwargs):
        """Создать новую роль"""
        role_args = role_args_parse(**kwargs)
        role = role_access.create(**role_args)

        return role, HTTPStatus.CREATED


@doc(tags=[tag])
class Role(MethodResource, Resource):
    """Получить, удалить, изменить роль по uuid"""

    @marshal_with(RoleSchema)
    @login_required(superuser=True)
    def get(self, uuid: UUID, **kwargs):
        """Получить роль по uuid"""
        role = role_access.get_by_id(uuid)
        return role, HTTPStatus.OK

    @use_kwargs(RoleSchema)
    @marshal_with(RoleSchema)
    @login_required(superuser=True)
    def put(self, uuid: UUID, **kwargs):
        """Изменение роли"""
        role_args = role_args_parse(**kwargs)
        role = role_access.update(uuid, **role_args)
        return role, HTTPStatus.OK

    @login_required(superuser=True)
    def delete(self, uuid: UUID, **kwargs):
        """Удаление роли"""
        role_access.delete(uuid)
        return {'message': 'Role is deleted'}, HTTPStatus.OK
