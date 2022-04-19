from http import HTTPStatus
from uuid import UUID

from flask_apispec import doc, marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from api.v1.serializers.permission import PermissionSchema
from db.access import PermissionAccess

permission_access = PermissionAccess()
tag = 'Permission'


@doc(tags=[tag])
class Permissions(MethodResource, Resource):
    """Показать список всех привилегий или создать новую"""

    @marshal_with(PermissionSchema(many=True))
    def get(self):
        """Получить список всех привилегий"""
        permissions = permission_access.get_all()
        return permissions, HTTPStatus.OK

    @use_kwargs(PermissionSchema)
    @marshal_with(PermissionSchema)
    def post(self, **kwargs):
        """Создать новую привилегию"""
        permission = permission_access.create(**kwargs)

        return permission, HTTPStatus.CREATED


@doc(tags=[tag])
class Permission(MethodResource, Resource):
    """Получить, удалить, изменить привилегию по uuid"""

    @marshal_with(PermissionSchema)
    def get(self, uuid: UUID):
        """Получить привилегии по uuid"""
        permission = permission_access.get_by_id(uuid)
        return permission, HTTPStatus.OK

    @use_kwargs(PermissionSchema)
    @marshal_with(PermissionSchema)
    def put(self, uuid: UUID, **kwargs):
        """Изменение привилегии"""
        permission = permission_access.update(uuid, **kwargs)
        return permission, HTTPStatus.OK

    def delete(self, uuid: UUID):
        """Удаление привилегии"""
        permission_access.delete(uuid)
        return {'message': 'Permission is deleted'}, HTTPStatus.OK
