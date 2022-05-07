from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from src.api.v1.serializers.permission import PermissionSchema
from src.api.v1.serializers.role_permission import (PermissionRoleSchema,
                                                    role_permission_args_parse)
from src.db.access import RoleAccess
from src.services.auth import login_required
from src.services.rate_limit import check_rate_limit

role_access = RoleAccess()
tag = 'Permission role'


@doc(tags=[tag])
class PermissionRole(MethodResource, Resource):
    """Получить все роли пользователя"""

    @marshal_with(PermissionSchema(many=True))
    @login_required()
    @check_rate_limit
    def get(self, role_uuid: UUID, **kwargs):
        """Получить список всех ролей"""
        permissions = role_access.get_role_permissions(role_uuid)
        return permissions, HTTPStatus.OK


@doc(tags=[tag])
class PermissionRoleManager(MethodResource, Resource):
    """Назначит или убрать у пользователя роль"""

    @use_kwargs(PermissionRoleSchema)
    @login_required(superuser=True)
    def post(self, **kwargs):
        """Выдать пользователю роль"""
        role_permission_args = role_permission_args_parse(**kwargs)
        role_access.add_permission(**role_permission_args)

        return {'message': 'Permission is added'}, HTTPStatus.CREATED

    @use_kwargs(PermissionRoleSchema)
    @login_required(superuser=True)
    def put(self, **kwargs):
        """Убрать у пользователя роль"""
        role_permission_args = role_permission_args_parse(**kwargs)
        role_access.remove_permission(**role_permission_args)

        return {'message': 'Permission is removed'}, HTTPStatus.OK
