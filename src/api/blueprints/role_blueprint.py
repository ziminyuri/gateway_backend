from flask import Blueprint
from flask_restful import Api

from src.api.v1.endpoints import (Permission, PermissionRole,
                                  PermissionRoleManager, Permissions, Role,
                                  Roles, UserRole, RoleUsers)
from src.core.config import BLUEPRINT_ROLE_API, URL_PREFIX

role_bp = Blueprint(BLUEPRINT_ROLE_API, __name__, url_prefix=URL_PREFIX)
role_api = Api(role_bp)

role_api.add_resource(Roles, '/role')
role_api.add_resource(Role, '/role/<uuid:uuid>')

role_api.add_resource(UserRole, '/role/user')
role_api.add_resource(RoleUsers, '/role/<int:role_id>/user')

role_api.add_resource(Permissions, '/permission')
role_api.add_resource(Permission, '/permission/<uuid:uuid>')

role_api.add_resource(PermissionRoleManager, '/permission/role')
role_api.add_resource(PermissionRole, '/permission/role/<uuid:role_uuid>')
