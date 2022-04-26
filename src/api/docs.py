from flask_apispec import FlaskApiSpec

from src.api.v1.endpoints import (AuthHistory, ChangePassword,
                                  ChangePersonalData, Login, Logout,
                                  Permission, PermissionRole,
                                  PermissionRoleManager, Permissions, Refresh,
                                  Registration, Role, Roles, UserRole,
                                  UserRoleManager)
from src.core.config import BLUEPRINT_API

docs = FlaskApiSpec()

docs.register(Roles, blueprint=BLUEPRINT_API)
docs.register(Role, blueprint=BLUEPRINT_API)
docs.register(UserRole, blueprint=BLUEPRINT_API)
docs.register(UserRoleManager, blueprint=BLUEPRINT_API)

docs.register(Permissions, blueprint=BLUEPRINT_API)
docs.register(Permission, blueprint=BLUEPRINT_API)
docs.register(PermissionRole, blueprint=BLUEPRINT_API)
docs.register(PermissionRoleManager, blueprint=BLUEPRINT_API)

docs.register(Login, blueprint=BLUEPRINT_API)
docs.register(Logout, blueprint=BLUEPRINT_API)
docs.register(Registration, blueprint=BLUEPRINT_API)
docs.register(Refresh, blueprint=BLUEPRINT_API)
docs.register(AuthHistory, blueprint=BLUEPRINT_API)
docs.register(ChangePersonalData, blueprint=BLUEPRINT_API)
docs.register(ChangePassword, blueprint=BLUEPRINT_API)
