from flask import Blueprint
from flask_restful import Api

from src.api.v1.endpoints import (Login, Logout, LogoutFromEverywhere,
                                  Permission, PermissionRole,
                                  PermissionRoleManager, Permissions, Refresh,
                                  Registration, Role, Roles, SecretResource,
                                  UserRole, UserRoleManager)
from src.core.config import BLUEPRINT_API, URL_PREFIX

blueprint = Blueprint(BLUEPRINT_API, __name__, url_prefix=URL_PREFIX)
api = Api(blueprint)

api.add_resource(Roles, '/role')
api.add_resource(Role, '/role/<uuid:uuid>')

api.add_resource(UserRole, '/user/role')
api.add_resource(UserRoleManager, '/user/role')

api.add_resource(Permissions, '/permission')
api.add_resource(Permission, '/permission/<uuid:uuid>')

api.add_resource(PermissionRoleManager, '/permission/role')
api.add_resource(PermissionRole, '/permission/role/<uuid:role_uuid>')

api.add_resource(Login, '/auth/login')
api.add_resource(Logout, '/auth/logout')
api.add_resource(LogoutFromEverywhere, '/auth/logout/device/all')
api.add_resource(Registration, '/auth/registration')
api.add_resource(Refresh, '/auth/refresh')
api.add_resource(SecretResource, '/auth/tests')
