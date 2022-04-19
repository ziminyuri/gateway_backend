from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from api.v1.serializers.role import RoleSchema
from api.v1.serializers.user_role import UserRoleSchema
from db.access import UserAccess

user_access = UserAccess()
tag = 'User roles'


@doc(tags=[tag])
class UserRole(MethodResource, Resource):
    """Получить все роли пользователя"""

    @marshal_with(RoleSchema(many=True))
    def get(self, uuid: UUID):
        """Получить список всех ролей"""
        roles = user_access.get_all_roles(uuid)
        return roles, HTTPStatus.OK


@doc(tags=[tag])
class UserRoleManager(MethodResource, Resource):
    """Назначит или убрать у пользователя роль"""

    @use_kwargs(UserRoleSchema)
    def post(self, **kwargs):
        """Выдать пользователю роль"""
        user_access.assign_role(**kwargs)

        return {'message': 'Role is assigned'}, HTTPStatus.CREATED

    @use_kwargs(UserRoleSchema)
    def put(self, **kwargs):
        """Убрать у пользователя роль"""
        user_access.remove_role(**kwargs)

        return {'message': 'Role is removed'}, HTTPStatus.OK
