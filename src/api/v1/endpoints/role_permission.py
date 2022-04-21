from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from api.v1.serializers.permission import PermissionSchema
from api.v1.serializers.role_permission import (PermissionRoleSchema,
                                                role_permission_args_parse)
from db.access import RoleAccess
from services.auth import login_required

role_access = RoleAccess()
tag = 'Permission role'


@doc(tags=[tag])
class PermissionRole(MethodResource, Resource):
    """Получить все роли пользователя"""

    @marshal_with(PermissionSchema(many=True))
    @login_required()
    def get(self, uuid: UUID, **kwargs):
        """Получить список всех ролей"""
        permissions = role_access.get_all_permissions(uuid)
        return permissions, HTTPStatus.OK


@doc(tags=[tag])
class PermissionRoleManager(MethodResource, Resource):
    """Назначит или убрать у пользователя роль"""

    @use_kwargs(PermissionRoleSchema)
    @login_required()
    def post(self, **kwargs):
        """Выдать пользователю роль"""
        role_permission_args = role_permission_args_parse(**kwargs)
        role_access.add_permission(**role_permission_args)

        return {'message': 'Permission is added'}, HTTPStatus.CREATED

    @use_kwargs(PermissionRoleSchema)
    @login_required()
    def put(self, **kwargs):
        """Убрать у пользователя роль"""
        role_permission_args = role_permission_args_parse(**kwargs)
        role_access.remove_permission(**role_permission_args)

        return {'message': 'Permission is removed'}, HTTPStatus.OK
