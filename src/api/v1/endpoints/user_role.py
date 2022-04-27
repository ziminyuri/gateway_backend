from http import HTTPStatus

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from src.api.v1.serializers.role import RoleSchema
from src.api.v1.serializers.user_role import (UserRoleSchema,
                                              role_user_args_parse)
from src.db.access import UserAccess
from src.services.auth import login_required

user_access = UserAccess()
tag = 'User roles'


@doc(tags=[tag])
class UserRole(MethodResource, Resource):
    """Получить все роли пользователя"""

    @marshal_with(RoleSchema(many=True))
    @login_required()
    def get(self, **kwargs):
        """Получить список всех ролей"""
        user_id = kwargs['user_id']
        roles = user_access.get_all_roles(user_id)
        return roles, HTTPStatus.OK

    @use_kwargs(UserRoleSchema)
    @login_required()
    def post(self, **kwargs):
        """Выдать пользователю роль"""
        role_user_args = role_user_args_parse(**kwargs)
        user_access.assign_role(**role_user_args)

        return {'message': 'Role is assigned'}, HTTPStatus.CREATED

    @use_kwargs(UserRoleSchema)
    @login_required()
    def put(self, **kwargs):
        """Убрать у пользователя роль"""
        role_user_args = role_user_args_parse(**kwargs)
        user_access.remove_role(**role_user_args)

        return {'message': 'Role is removed'}, HTTPStatus.OK
