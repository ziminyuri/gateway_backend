from flask import Blueprint
from flask_restful import Api

from api.v1.endpoints import (Permission, Permissions, Role, Roles, UserRole,
                              UserRoleManager)
from core.config import BLUEPRINT_API, URL_PREFIX

blueprint = Blueprint(BLUEPRINT_API, __name__, url_prefix=URL_PREFIX)
api = Api(blueprint)

api.add_resource(Roles, '/role')
api.add_resource(Role, '/role/<uuid:uuid>')
api.add_resource(UserRole, '/user/role/<uuid:uuid>')
api.add_resource(UserRoleManager, '/user/role')
api.add_resource(Permissions, '/permission')
api.add_resource(Permission, '/permission/<uuid:uuid>')
