from flask_apispec import FlaskApiSpec

from src.api.v1.endpoints import (AuthHistory, ChangePassword, Login, Logout,
                                  Permission, PermissionRole,
                                  PermissionRoleManager, Permissions, Refresh,
                                  Registration, Role, Roles,
                                  TwoFactorAuthentication, UserRole)
from src.core.config import BLUEPRINT_AUTH_API, BLUEPRINT_ROLE_API

docs = FlaskApiSpec()

docs.register(Roles, blueprint=BLUEPRINT_ROLE_API)
docs.register(Role, blueprint=BLUEPRINT_ROLE_API)

docs.register(Permissions, blueprint=BLUEPRINT_ROLE_API)
docs.register(Permission, blueprint=BLUEPRINT_ROLE_API)
docs.register(PermissionRole, blueprint=BLUEPRINT_ROLE_API)
docs.register(PermissionRoleManager, blueprint=BLUEPRINT_ROLE_API)

docs.register(UserRole, blueprint=BLUEPRINT_AUTH_API)

docs.register(Login, blueprint=BLUEPRINT_AUTH_API)
docs.register(Logout, blueprint=BLUEPRINT_AUTH_API)
docs.register(Registration, blueprint=BLUEPRINT_AUTH_API)
docs.register(Refresh, blueprint=BLUEPRINT_AUTH_API)
docs.register(AuthHistory, blueprint=BLUEPRINT_AUTH_API)
docs.register(TwoFactorAuthentication, blueprint=BLUEPRINT_AUTH_API)
docs.register(ChangePassword, blueprint=BLUEPRINT_AUTH_API)
