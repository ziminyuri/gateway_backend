from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from api.v1.serializers.permission import PermissionSchema
from api.v1.serializers.role_permission import PermissionRoleSchema
from db.access import RoleAccess

role_access = RoleAccess()
tag = 'Permission role'


@doc(tags=[tag])
class PermissionRole(MethodResource, Resource):
    """Получить все роли пользователя"""

    @marshal_with(PermissionSchema(many=True))
    def get(self, uuid: UUID):
        """Получить список всех ролей"""
        permissions = role_access.get_all_permissions(uuid)
        return permissions, HTTPStatus.OK


@doc(tags=[tag])
class PermissionRoleManager(MethodResource, Resource):
    """Назначит или убрать у пользователя роль"""

    @use_kwargs(PermissionRoleSchema)
    def post(self, **kwargs):
        """Выдать пользователю роль"""
        role_access.add_permission(**kwargs)

        return {'message': 'Permission is added'}, HTTPStatus.CREATED

    @use_kwargs(PermissionRoleSchema)
    def put(self, **kwargs):
        """Убрать у пользователя роль"""
        role_access.remove_permission(**kwargs)

        return {'message': 'Permission is removed'}, HTTPStatus.OK
